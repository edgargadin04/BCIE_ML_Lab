"""
Capa Bronze — Extracción de Datos.

Extrae datos crudos de la API CKAN del BCIE y los almacena
en la capa Bronze de la arquitectura Medallón.
"""

import pandas as pd
import requests
from pathlib import Path
from typing import Dict, Any

from core.logger import get_logger
from core import config as cfg

logger = get_logger(__name__)


def extract_from_api(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extrae datos de la API CKAN del BCIE.

    Args:
        config: Configuración del proyecto.

    Returns:
        DataFrame con los registros crudos.

    Raises:
        ConnectionError: Si la API no responde y no hay caché local.
    """
    api = config["api"]
    url = api["base_url"]
    params = {"resource_id": api["resource_id"], "limit": api["limit"]}
    timeout = api.get("timeout", 30)

    logger.info(f"Conectando a API BCIE: {url}")

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()

        data = response.json()
        if not data.get("success"):
            raise ConnectionError("API retornó success=false")

        records = data["result"]["records"]
        df = pd.DataFrame(records)
        logger.info(f"Extracción exitosa: {len(df):,} registros descargados")
        return df

    except Exception as e:
        logger.warning(f"Error en API: {e}. Buscando caché local...")
        return _load_from_cache(config)


def _load_from_cache(config: Dict[str, Any]) -> pd.DataFrame:
    """Intenta cargar datos de la caché Bronze local."""
    bronze_dir = Path(config["paths"]["bronze"])
    fmt = config["paths"].get("format", "parquet")

    cache_path = bronze_dir / f"aprobaciones_raw.{fmt}"

    if cache_path.exists():
        df = _read_file(cache_path, fmt)
        logger.info(f"Caché cargada: {len(df):,} registros desde {cache_path}")
        return df

    # Fallback: buscar cualquier formato
    for ext in ["parquet", "csv"]:
        alt_path = bronze_dir / f"aprobaciones_raw.{ext}"
        if alt_path.exists():
            df = _read_file(alt_path, ext)
            logger.info(f"Caché alternativa: {len(df):,} registros desde {alt_path}")
            return df

    raise FileNotFoundError("No se encontró caché local en capa Bronze.")


def save_bronze(df: pd.DataFrame, config: Dict[str, Any]) -> Path:
    """
    Guarda los datos crudos en la capa Bronze.

    Args:
        df: DataFrame crudo de la API.
        config: Configuración del proyecto.

    Returns:
        Ruta al archivo guardado.
    """
    bronze_dir = Path(config["paths"]["bronze"])
    bronze_dir.mkdir(parents=True, exist_ok=True)

    fmt = config["paths"].get("format", "parquet")
    output_path = bronze_dir / f"aprobaciones_raw.{fmt}"

    _write_file(df, output_path, fmt)
    logger.info(f"Bronze guardado: {output_path} ({len(df):,} registros)")

    return output_path


def run_bronze(config: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Ejecuta la capa Bronze completa: extrae y guarda.

    Args:
        config: Configuración. Si es None, carga desde archivo.

    Returns:
        DataFrame con datos crudos.
    """
    if config is None:
        config = cfg.get_config()

    logger.info("━━━ CAPA BRONZE: EXTRACCIÓN ━━━")
    df = extract_from_api(config)
    save_bronze(df, config)

    return df


# --- Utilidades de I/O ---

def _read_file(path: Path, fmt: str) -> pd.DataFrame:
    """Lee archivo en formato parquet o csv."""
    if fmt == "parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _write_file(df: pd.DataFrame, path: Path, fmt: str) -> None:
    """Escribe DataFrame en formato parquet o csv."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "parquet":
        df.to_parquet(path, index=False, engine="pyarrow")
    else:
        df.to_csv(path, index=False, encoding="utf-8")
