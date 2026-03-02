"""Modelo HDBSCAN."""

import numpy as np
import hdbscan
from clustering.base import ClusteringModel


class HDBSCANModel(ClusteringModel):
    name = "hdbscan"
    display_name = "HDBSCAN"

    def fit_predict(self, X_scaled: np.ndarray) -> np.ndarray:
        self.model = hdbscan.HDBSCAN(
            min_cluster_size=self.model_config.get("min_cluster_size", 15),
            min_samples=self.model_config.get("min_samples", 5),
            metric=self.model_config.get("metric", "euclidean"),
            gen_min_span_tree=True,
        )
        labels = self.model.fit_predict(X_scaled)
        return labels

    def _fit_predict_for_bootstrap(self, X, seed):
        model = hdbscan.HDBSCAN(
            min_cluster_size=self.model_config.get("min_cluster_size", 15),
            min_samples=self.model_config.get("min_samples", 5),
            metric=self.model_config.get("metric", "euclidean"),
        )
        return model.fit_predict(X)

    def _add_extra_columns(self, df, X_scaled):
        if hasattr(self.model, "probabilities_"):
            df["Probabilidad"] = self.model.probabilities_
        if hasattr(self.model, "outlier_scores_"):
            df["Outlier_Score"] = self.model.outlier_scores_
        return df
