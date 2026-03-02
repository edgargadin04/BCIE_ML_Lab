"""Modelo Gaussian Mixture (GMM)."""

import numpy as np
from sklearn.mixture import GaussianMixture
from clustering.base import ClusteringModel
from core.logger import get_logger

logger = get_logger(__name__)


class GMMModel(ClusteringModel):
    name = "gmm"
    display_name = "Gaussian Mixture Model"

    def fit_predict(self, X_scaled: np.ndarray) -> np.ndarray:
        optimal_k = self.model_config.get("optimal_k", 0)
        covariance = self.model_config.get("covariance_type", "full")

        if optimal_k == 0:
            optimal_k = self._auto_select_k(X_scaled, covariance)

        self.model = GaussianMixture(
            n_components=optimal_k,
            covariance_type=covariance,
            random_state=self.random_state,
            n_init=5,
        )
        self.model.fit(X_scaled)
        labels = self.model.predict(X_scaled)
        self.probabilities_ = self.model.predict_proba(X_scaled)
        return labels

    def _auto_select_k(self, X_scaled, covariance):
        """Selección automática de K por BIC."""
        max_k = self.cluster_config.get("max_k", 10)
        best_k, best_bic = 2, float("inf")
        for k in range(2, max_k + 1):
            gm = GaussianMixture(n_components=k, covariance_type=covariance,
                                 random_state=self.random_state, n_init=3)
            gm.fit(X_scaled)
            bic = gm.bic(X_scaled)
            if bic < best_bic:
                best_bic, best_k = bic, k
        logger.info(f"  Auto K (BIC): {best_k}")
        return best_k

    def _fit_predict_for_bootstrap(self, X, seed):
        k = len(np.unique(self.labels_[self.labels_ >= 0]))
        model = GaussianMixture(n_components=k, random_state=seed, n_init=3)
        return model.fit_predict(X)

    def _add_extra_columns(self, df, X_scaled):
        probs = self.probabilities_
        df["Probabilidad_Max"] = probs.max(axis=1)
        df["Entropia"] = -(probs * np.log(probs + 1e-10)).sum(axis=1)
        return df

    def get_optimization_data(self, X_scaled):
        max_k = self.cluster_config.get("max_k", 10)
        covariance = self.model_config.get("covariance_type", "full")
        data = []
        for k in range(1, max_k + 1):
            gm = GaussianMixture(n_components=k, covariance_type=covariance,
                                 random_state=self.random_state, n_init=3)
            gm.fit(X_scaled)
            data.append({"k": k, "aic": float(gm.aic(X_scaled)), "bic": float(gm.bic(X_scaled))})
        return data
