"""Modelo Clustering Jerárquico (Agglomerative Ward)."""

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from clustering.base import ClusteringModel


class HierarchicalModel(ClusteringModel):
    name = "hierarchical"
    display_name = "Clustering Jerárquico (Ward)"

    def fit_predict(self, X_scaled: np.ndarray) -> np.ndarray:
        n_clusters = self.model_config.get("n_clusters", 4)
        linkage = self.model_config.get("linkage", "ward")

        self.model = AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage=linkage,
        )
        return self.model.fit_predict(X_scaled)

    def _fit_predict_for_bootstrap(self, X, seed):
        n_clusters = self.model_config.get("n_clusters", 4)
        linkage = self.model_config.get("linkage", "ward")
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        return model.fit_predict(X)

    def get_optimization_data(self, X_scaled):
        max_k = self.cluster_config.get("max_k", 10)
        linkage = self.model_config.get("linkage", "ward")
        data = []
        for k in range(2, max_k + 1):
            model = AgglomerativeClustering(n_clusters=k, linkage=linkage)
            labels = model.fit_predict(X_scaled)
            from sklearn.metrics import silhouette_score
            data.append({
                "k": k,
                "silhouette": float(silhouette_score(X_scaled, labels)),
            })
        return data
