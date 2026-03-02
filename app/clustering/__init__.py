"""Registro de modelos de clustering."""

from clustering.kmeans import KMeansModel
from clustering.kmedoids import KMedoidsModel
from clustering.hdbscan_model import HDBSCANModel
from clustering.dbscan_model import DBSCANModel
from clustering.hierarchical import HierarchicalModel
from clustering.gmm import GMMModel
from clustering.mixed import MixedModel

CLUSTERING_MODELS = {
    "kmeans": KMeansModel,
    "kmedoids": KMedoidsModel,
    "hdbscan": HDBSCANModel,
    "dbscan": DBSCANModel,
    "hierarchical": HierarchicalModel,
    "gmm": GMMModel,
    "mixed": MixedModel,
}


def get_enabled_models(config):
    """Retorna solo los modelos habilitados en la configuración."""
    enabled = {}
    for name, cls in CLUSTERING_MODELS.items():
        model_cfg = config["clustering"]["models"].get(name, {})
        if model_cfg.get("enabled", False):
            enabled[name] = cls
    return enabled
