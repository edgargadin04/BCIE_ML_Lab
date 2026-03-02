"""
Módulo de Configuración.

Carga y provee acceso centralizado al archivo config.yaml.
"""

import yaml
from pathlib import Path
from typing import Any, Dict

_config: Dict[str, Any] = {}


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Carga la configuración desde el YAML.

    Args:
        config_path: Ruta al archivo YAML. Si es None, busca config.yaml
                     en el directorio raíz de la app.

    Returns:
        Diccionario con toda la configuración.
    """
    global _config

    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"

    with open(config_path, "r", encoding="utf-8") as f:
        _config = yaml.safe_load(f)

    return _config


def get_config() -> Dict[str, Any]:
    """Retorna la configuración cargada."""
    if not _config:
        load_config()
    return _config


def get(key_path: str, default: Any = None) -> Any:
    """
    Accede a la configuración por ruta separada por puntos.

    Ejemplo:
        get('clustering.models.kmeans.optimal_k')  → 3
        get('paths.bronze')  → 'data/bronze'

    Args:
        key_path: Ruta separada por puntos.
        default: Valor por defecto si no existe.

    Returns:
        Valor de la configuración o default.
    """
    cfg = get_config()
    keys = key_path.split(".")
    for key in keys:
        if isinstance(cfg, dict) and key in cfg:
            cfg = cfg[key]
        else:
            return default
    return cfg
