"""Modelo DBSCAN."""

import numpy as np
from sklearn.cluster import DBSCAN
from clustering.base import ClusteringModel


class DBSCANModel(ClusteringModel):
    name = "dbscan"
    display_name = "DBSCAN"

    def fit_predict(self, X_scaled: np.ndarray) -> np.ndarray:
        self.model = DBSCAN(
            eps=self.model_config.get("eps", 0.25),
            min_samples=self.model_config.get("min_samples", 10),
            metric=self.model_config.get("metric", "euclidean"),
        )
        return self.model.fit_predict(X_scaled)

    def _fit_predict_for_bootstrap(self, X, seed):
        model = DBSCAN(
            eps=self.model_config.get("eps", 0.25),
            min_samples=self.model_config.get("min_samples", 10),
            metric=self.model_config.get("metric", "euclidean"),
        )
        return model.fit_predict(X)

    def _add_extra_columns(self, df, X_scaled):
        labels = self.labels_
        # Core samples
        core_mask = np.zeros(len(labels), dtype=bool)
        if hasattr(self.model, "core_sample_indices_"):
            core_mask[self.model.core_sample_indices_] = True
        df["Es_Core"] = core_mask
        return df
