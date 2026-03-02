"""Modelo Mixed Clustering (Gower + Jerárquico)."""

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from clustering.base import ClusteringModel
from core.logger import get_logger

logger = get_logger(__name__)


class MixedModel(ClusteringModel):
    name = "mixed"
    display_name = "Mixed Clustering (Gower)"

    def run(self, df: pd.DataFrame):
        """Override del run base porque Mixed usa features mixtas."""
        logger.info(f"▶ {self.display_name}")

        # Preparar features mixtas
        X_gower, df_valid = self._prepare_mixed_features(df)

        # Clustering jerárquico sobre distancia Gower
        labels = self._cluster_on_distance(X_gower)
        self.labels_ = labels
        self.X_scaled_ = X_gower

        # Métricas (sobre la matriz de distancia)
        from core.metrics import compute_clustering_metrics
        k = len(np.unique(labels[labels >= 0]))
        self.metrics_ = compute_clustering_metrics(
            X_scaled=X_gower, labels=labels, k=k,
            model_name=self.name, bootstrap_n=0,
        )

        # Resultados
        df_result = df_valid.copy()
        df_result["Cluster"] = labels
        self._save_gold(df_result, self.metrics_)
        return df_result, self.metrics_

    def _prepare_mixed_features(self, df):
        """Prepara features numéricas + categóricas para distancia Gower."""
        import gower

        num_features = self.features
        cat_features = self.model_config.get("categorical_features", [])
        all_features = num_features + [c for c in cat_features if c in df.columns]

        df_valid = df[all_features].dropna()

        # Calcular matriz de distancia Gower
        cat_mask = [c in cat_features for c in df_valid.columns]
        dist_matrix = gower.gower_matrix(df_valid, cat_features=cat_mask)

        logger.info(f"  Gower: {len(df_valid)} muestras, {len(all_features)} features "
                     f"({sum(cat_mask)} categóricas)")

        return dist_matrix, df.loc[df_valid.index]

    def _cluster_on_distance(self, dist_matrix):
        """Clustering jerárquico sobre la matriz de distancia Gower."""
        from sklearn.cluster import AgglomerativeClustering

        best_k, best_sil = 2, -1
        max_k = min(self.cluster_config.get("max_k", 10), len(dist_matrix) - 1)

        for k in range(2, max_k + 1):
            model = AgglomerativeClustering(
                n_clusters=k, metric="precomputed", linkage="average"
            )
            labels = model.fit_predict(dist_matrix)
            from sklearn.metrics import silhouette_score
            sil = silhouette_score(dist_matrix, labels, metric="precomputed")
            if sil > best_sil:
                best_sil, best_k = sil, k

        logger.info(f"  K óptimo (Gower): {best_k} (Silhouette={best_sil:.4f})")

        final_model = AgglomerativeClustering(
            n_clusters=best_k, metric="precomputed", linkage="average"
        )
        return final_model.fit_predict(dist_matrix)

    def fit_predict(self, X_scaled):
        """No utilizado en Mixed — se usa run() directamente."""
        pass
