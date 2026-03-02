"""
Capa Silver — Limpieza, Transformación y Agregación.

Transforma los datos crudos (Bronze) en tablas limpias listas para
modelado. Produce dos vistas principales:
  - Agregación País-Año (para Clustering)
  - Serie Temporal (para Forecasting)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple

from core.logger import get_logger
from core import config as cfg

logger = get_logger(__name__)


def clean_data(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Limpia y estandariza los datos crudos.

    Operaciones:
      1. Renombrado de columnas
      2. Conversión de tipos
      3. Estandarización de strings (UPPER)
      4. Ingeniería de fechas
      5. Eliminación de nulos

    Args:
        df: DataFrame crudo (Bronze).
        config: Configuración del proyecto.

    Returns:
        DataFrame limpio.
    """
    logger.info("Limpiando datos...")

    # 1. Renombrar columnas
    rename_map = config["columns"]["rename"]
    df = df.rename(columns=rename_map)

    # 2. Columna de valor numérica
    val_col = config["columns"]["value_col"]
    df[val_col] = pd.to_numeric(df[val_col], errors="coerce")

    # 3. Estandarizar strings
    group_col = config["columns"]["group_col"]
    if group_col in df.columns:
        df[group_col] = df[group_col].astype(str).str.upper().str.strip()

    if "Sector" in df.columns:
        df["Sector"] = df["Sector"].astype(str).str.strip().str.title()

    # 4. Ingeniería de fechas
    if "Anio" in df.columns:
        df["Fecha"] = pd.to_datetime(df["Anio"].astype(int).astype(str) + "-01-01")
        df["Anio"] = df["Anio"].astype(int)
    else:
        raise KeyError("Columna 'Anio' no encontrada después del renombrado.")

    # 5. Eliminar nulos en columnas críticas
    n_before = len(df)
    df = df.dropna(subset=["Fecha", val_col])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        logger.warning(f"Se eliminaron {n_dropped} registros con valores nulos.")

    logger.info(f"Datos limpios: {len(df):,} registros")
    return df


def aggregate_for_clustering(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Agrega datos a nivel País-Año para Clustering.

    Genera:
      - Monto total aprobado por País-Año
      - Cantidad de aprobaciones por País-Año
      - Sector predominante
      - Clasificación de tipo de país
      - Bandas de monto y frecuencia

    Args:
        df: DataFrame limpio.
        config: Configuración del proyecto.

    Returns:
        DataFrame agregado a nivel País-Año.
    """
    logger.info("Generando agregación País-Año para clustering...")

    group_col = config["columns"]["group_col"]
    val_col = config["columns"]["value_col"]

    # Columna de conteo
    count_col = "_id" if "_id" in df.columns else "__count"
    if count_col == "__count":
        df["__count"] = 1

    # Top sector por grupo
    def top_sector(x):
        return x.value_counts().index[0] if len(x) > 0 else "Desconocido"

    df_agg = (
        df.groupby([group_col, "Anio"])
        .agg(
            Monto_Aprobado=(val_col, "sum"),
            Cantidad_Aprobaciones=(count_col, "count"),
            Sector=("Sector", top_sector),
        )
        .reset_index()
    )

    # --- Features adicionales ---

    # Tipo de país
    fundadores = config.get("paises_fundadores", [])
    df_agg["Tipo_Pais"] = df_agg[group_col].apply(
        lambda p: "Regional" if p in fundadores
        else ("Multi-country" if p == "REGIONAL" else "Extra-regional")
    )

    # Década
    df_agg["Decada"] = (df_agg["Anio"] // 10 * 10).astype(str) + "s"

    # Bandas de monto (cuartiles)
    m_pos = df_agg.loc[df_agg["Monto_Aprobado"] > 0, "Monto_Aprobado"]
    if len(m_pos) > 0:
        q_med = m_pos.median()
        q_p95 = m_pos.quantile(0.95)
        df_agg["Monto_Banda"] = pd.cut(
            df_agg["Monto_Aprobado"],
            bins=[0, q_med, q_p95, float("inf")],
            labels=["Menor", "Regular", "Estrategico"],
            include_lowest=True,
        ).astype(str)

    # Bandas de frecuencia
    def freq_band(x):
        if x == 1: return "Ocasional"
        if x <= 3: return "Baja"
        if x <= 6: return "Media"
        return "Alta"

    df_agg["Frecuencia_Banda"] = df_agg["Cantidad_Aprobaciones"].apply(freq_band)

    # Cuadrante estratégico
    med_monto = df_agg["Monto_Aprobado"].median()
    med_freq = df_agg["Cantidad_Aprobaciones"].median()
    df_agg["Cuadrante"] = df_agg.apply(
        lambda r: (
            "Core Estrategico" if r["Monto_Aprobado"] >= med_monto and r["Cantidad_Aprobaciones"] >= med_freq
            else "Big Deals" if r["Monto_Aprobado"] >= med_monto
            else "Operativo" if r["Cantidad_Aprobaciones"] >= med_freq
            else "Oportunidad"
        ),
        axis=1,
    )

    logger.info(f"Agregación completada: {len(df_agg):,} registros País-Año")
    return df_agg


def aggregate_for_forecasting(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Agrega datos en formato serie temporal para Forecasting.

    Produce un DataFrame con columnas: Pais, Fecha, Monto_Aprobado
    (agrupado por año).

    Args:
        df: DataFrame limpio.
        config: Configuración del proyecto.

    Returns:
        DataFrame de series temporales.
    """
    logger.info("Generando series temporales para forecasting...")

    group_col = config["columns"]["group_col"]
    val_col = config["columns"]["value_col"]

    df_ts = (
        df.groupby([group_col, "Fecha"])[val_col]
        .sum()
        .reset_index()
        .sort_values(["Fecha", group_col])
    )

    df_ts.columns = ["Pais", "ds", "y"]

    n_paises = df_ts["Pais"].nunique()
    logger.info(f"Series temporales: {n_paises} países, {len(df_ts):,} puntos")
    return df_ts


def save_silver(
    df_clean: pd.DataFrame,
    df_clustering: pd.DataFrame,
    df_forecasting: pd.DataFrame,
    config: Dict[str, Any],
) -> None:
    """Guarda las tablas Silver en disco."""
    silver_dir = Path(config["paths"]["silver"])
    silver_dir.mkdir(parents=True, exist_ok=True)
    fmt = config["paths"].get("format", "parquet")

    tables = {
        "aprobaciones_limpias": df_clean,
        "aprobaciones_clustering": df_clustering,
        "aprobaciones_forecasting": df_forecasting,
    }

    for name, df in tables.items():
        path = silver_dir / f"{name}.{fmt}"
        if fmt == "parquet":
            df.to_parquet(path, index=False, engine="pyarrow")
        else:
            df.to_csv(path, index=False, encoding="utf-8")
        logger.info(f"  Silver → {path.name} ({len(df):,} registros)")


def run_silver(df_bronze: pd.DataFrame, config: Dict[str, Any] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Ejecuta la capa Silver completa.

    Args:
        df_bronze: DataFrame crudo de Bronze.
        config: Configuración.

    Returns:
        Tupla (df_clustering, df_forecasting).
    """
    if config is None:
        config = cfg.get_config()

    logger.info("━━━ CAPA SILVER: TRANSFORMACIÓN ━━━")

    df_clean = clean_data(df_bronze, config)
    df_clustering = aggregate_for_clustering(df_clean, config)
    df_forecasting = aggregate_for_forecasting(df_clean, config)

    save_silver(df_clean, df_clustering, df_forecasting, config)

    return df_clustering, df_forecasting
