"""
Métricas Estandarizadas de Clustering.

Provee un cálculo unificado de todas las métricas de evaluación,
incluyendo análisis de estabilidad bootstrap.
"""

import numpy as np
from sklearn.metrics import (
    silhouette_score,
    silhouette_samples,
    davies_bouldin_score,
    calinski_harabasz_score,
    adjusted_rand_score,
)
from sklearn.utils import resample
from typing import Dict, Any

from core.logger import get_logger

logger = get_logger(__name__)


def compute_clustering_metrics(
    X_scaled: np.ndarray,
    labels: np.ndarray,
    k: int,
    model_name: str,
    bootstrap_n: int = 20,
    fit_predict_fn=None,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Calcula todas las métricas estándar para un modelo de clustering.

    Args:
        X_scaled: Datos escalados (n_samples, n_features).
        labels: Asignaciones de cluster.
        k: Número de clusters resultantes.
        model_name: Nombre del modelo para logging.
        bootstrap_n: Número de iteraciones bootstrap para estabilidad.
        fit_predict_fn: Función que recibe (X, random_state) y retorna labels.
                        Usada para bootstrap. Si es None, no se calcula estabilidad.
        random_state: Semilla base.

    Returns:
        Diccionario con todas las métricas.
    """
    metrics = {"modelo": model_name, "k": int(k)}

    # --- Métricas Básicas ---
    valid_mask = labels >= 0  # Excluir noise (-1) para HDBSCAN/DBSCAN
    n_valid = valid_mask.sum()

    if n_valid < 2 or len(np.unique(labels[valid_mask])) < 2:
        logger.warning(f"{model_name}: Insuficientes clusters válidos para métricas.")
        metrics.update({
            "silhouette": None,
            "davies_bouldin": None,
            "calinski_harabasz": None,
        })
        return metrics

    X_valid = X_scaled[valid_mask]
    labels_valid = labels[valid_mask]

    sil = silhouette_score(X_valid, labels_valid)
    dbi = davies_bouldin_score(X_valid, labels_valid)
    chi = calinski_harabasz_score(X_valid, labels_valid)

    metrics.update({
        "silhouette": round(sil, 4),
        "davies_bouldin": round(dbi, 4),
        "calinski_harabasz": round(chi, 2),
    })

    # --- Silhouette por muestra (% negativo) ---
    sil_samples = silhouette_samples(X_valid, labels_valid)
    neg_pct = float((sil_samples < 0).sum() / len(sil_samples) * 100)
    metrics["neg_silhouette_pct"] = round(neg_pct, 2)

    # --- Balance de Clusters ---
    unique, counts = np.unique(labels_valid, return_counts=True)
    size_cv = float(np.std(counts) / np.mean(counts))
    metrics.update({
        "size_cv": round(size_cv, 4),
        "min_cluster_pct": round(float(counts.min() / len(labels_valid) * 100), 1),
        "max_cluster_pct": round(float(counts.max() / len(labels_valid) * 100), 1),
        "cluster_sizes": {int(c): int(n) for c, n in zip(unique, counts)},
    })

    # --- Noise (para DBSCAN/HDBSCAN) ---
    n_noise = int((labels == -1).sum())
    if n_noise > 0:
        metrics["noise_pct"] = round(n_noise / len(labels) * 100, 2)
        metrics["noise_count"] = n_noise

    # --- Estabilidad Bootstrap ---
    if fit_predict_fn is not None and bootstrap_n > 0:
        logger.info(f"  Análisis de estabilidad ({bootstrap_n} iteraciones)...")
        ari_scores = []
        sil_boot = []

        for i in range(bootstrap_n):
            seed = random_state + i
            X_boot, _ = resample(X_valid, labels_valid, random_state=seed)
            try:
                labels_boot = fit_predict_fn(X_boot, seed)
                labels_pred = fit_predict_fn(X_valid, seed)
                ari = adjusted_rand_score(labels_valid, labels_pred)
                ari_scores.append(ari)
                if len(np.unique(labels_boot)) > 1:
                    sil_boot.append(silhouette_score(X_boot, labels_boot))
            except Exception:
                continue

        if ari_scores:
            metrics.update({
                "stability_ari": round(float(np.mean(ari_scores)), 4),
                "stability_std": round(float(np.std(ari_scores)), 4),
                "ari_min": round(float(np.min(ari_scores)), 4),
                "ari_max": round(float(np.max(ari_scores)), 4),
            })

        if sil_boot:
            metrics.update({
                "silhouette_mean": round(float(np.mean(sil_boot)), 4),
                "silhouette_std": round(float(np.std(sil_boot)), 4),
            })

    logger.info(f"  {model_name}: Silhouette={metrics.get('silhouette')}, "
                f"DBI={metrics.get('davies_bouldin')}, K={k}")

    return metrics
