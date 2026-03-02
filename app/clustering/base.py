"""
Clase Base Abstracta para Modelos de Clustering.

Todos los modelos de clustering heredan de esta clase,
garantizando una interfaz uniforme.
"""

import numpy as np
import pandas as pd
import json
from abc import ABC, abstractmethod
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, Optional, Tuple

from core.logger import get_logger
from core.metrics import compute_clustering_metrics

logger = get_logger(__name__)


class ClusteringModel(ABC):
    """Interfaz base para modelos de clustering."""

    name: str = "base"
    display_name: str = "Base Model"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cluster_config = config["clustering"]
        self.model_config = config["clustering"]["models"].get(self.name, {})
        self.features = self.cluster_config["features"]
        self.random_state = self.cluster_config.get("random_state", 42)
        self.scaler = StandardScaler()
        self.labels_ = None
        self.metrics_ = None
        self.X_scaled_ = None

    def run(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Ejecuta el pipeline completo: preparar → entrenar → evaluar → exportar.

        Args:
            df: DataFrame agregado (Silver clustering).

        Returns:
            Tupla (DataFrame con clusters, métricas).
        """
        logger.info(f"▶ {self.display_name}")

        # 1. Preparar features
        X, df_valid = self._prepare_features(df)

        # 2. Entrenar modelo
        labels = self.fit_predict(X)
        self.labels_ = labels
        self.X_scaled_ = X

        # 3. Calcular métricas
        k = len(np.unique(labels[labels >= 0]))
        self.metrics_ = compute_clustering_metrics(
            X_scaled=X,
            labels=labels,
            k=k,
            model_name=self.name,
            bootstrap_n=self.cluster_config.get("bootstrap_n", 20),
            fit_predict_fn=self._fit_predict_for_bootstrap,
            random_state=self.random_state,
        )

        # 4. Agregar resultados al DataFrame
        df_result = df_valid.copy()
        df_result["Cluster"] = labels
        df_result = self._add_extra_columns(df_result, X)

        # 5. Guardar resultados (Gold)
        self._save_gold(df_result, self.metrics_)

        return df_result, self.metrics_

    def _prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame]:
        """Prepara y escala las features para clustering."""
        df_valid = df[self.features].dropna()
        X = df_valid.copy()

        # Log transform
        log_col = self.cluster_config.get("log_transform_col")
        if log_col and log_col in X.columns:
            X[log_col] = np.log1p(X[log_col])

        X_scaled = self.scaler.fit_transform(X)

        logger.info(f"  Features: {self.features} | Muestras: {len(X_scaled):,}")
        return X_scaled, df.loc[df_valid.index]

    @abstractmethod
    def fit_predict(self, X_scaled: np.ndarray) -> np.ndarray:
        """Entrena el modelo y retorna labels. Cada modelo lo implementa."""
        ...

    def _fit_predict_for_bootstrap(self, X: np.ndarray, seed: int) -> np.ndarray:
        """Versión reusable para bootstrap. Override si el modelo lo necesita."""
        return self.fit_predict(X)

    def _add_extra_columns(self, df: pd.DataFrame, X_scaled: np.ndarray) -> pd.DataFrame:
        """Hook para agregar columnas extra específicas del modelo."""
        return df

    def _save_gold(self, df_result: pd.DataFrame, metrics: Dict) -> None:
        """Guarda resultados y métricas en la capa Gold."""
        gold_dir = Path(self.config["paths"]["gold"]) / "clustering" / self.name
        gold_dir.mkdir(parents=True, exist_ok=True)
        fmt = self.config["paths"].get("format", "parquet")

        # Guardar asignaciones
        result_path = gold_dir / f"resultados.{fmt}"
        if fmt == "parquet":
            df_result.to_parquet(result_path, index=False, engine="pyarrow")
        else:
            df_result.to_csv(result_path, index=False, encoding="utf-8")

        # Guardar métricas
        metrics_path = gold_dir / "metricas.json"
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"  Gold → {gold_dir.name}/ ({len(df_result):,} registros)")

    def get_optimization_data(self, X_scaled: np.ndarray) -> list:
        """
        Calcula métricas de validación para rango K=1..max_k.
        Override para algoritmos sin K (HDBSCAN, DBSCAN).
        """
        return []
