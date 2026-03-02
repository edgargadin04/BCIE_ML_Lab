"""Modelo K-Medoids."""

import numpy as np
from sklearn_extra.cluster import KMedoids
from clustering.base import ClusteringModel


class KMedoidsModel(ClusteringModel):
    name = "kmedoids"
    display_name = "K-Medoids"

    def fit_predict(self, X_scaled: np.ndarray) -> np.ndarray:
        k = self.model_config.get("optimal_k", 3)
        self.model = KMedoids(
            n_clusters=k,
            init="k-medoids++",
            random_state=self.random_state,
        )
        return self.model.fit_predict(X_scaled)

    def _fit_predict_for_bootstrap(self, X, seed):
        k = self.model_config.get("optimal_k", 3)
        model = KMedoids(n_clusters=k, init="k-medoids++", random_state=seed)
        return model.fit_predict(X)

    def _add_extra_columns(self, df, X_scaled):
        labels = self.labels_
        centers = self.model.cluster_centers_
        dist = np.linalg.norm(X_scaled - centers[labels], axis=1)
        df["Distancia_Centroide"] = dist
        return df

    def get_optimization_data(self, X_scaled):
        max_k = self.cluster_config.get("max_k", 10)
        data = []
        for k in range(1, max_k + 1):
            km = KMedoids(n_clusters=k, init="k-medoids++", random_state=self.random_state)
            labels = km.fit_predict(X_scaled)
            entry = {"k": k, "wcss": float(km.inertia_)}
            if k > 1:
                from sklearn.metrics import silhouette_score
                entry["silhouette"] = float(silhouette_score(X_scaled, labels))
            data.append(entry)
        return data
