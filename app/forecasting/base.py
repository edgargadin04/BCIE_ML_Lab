"""
Clase Base para Modelos de Forecasting.

Todos los modelos de forecasting heredan de esta clase.
Cada modelo implementa _train_country() con su lógica específica.
"""

import pandas as pd
import numpy as np
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List
from concurrent.futures import ProcessPoolExecutor, as_completed

from core.logger import get_logger

logger = get_logger(__name__)


class ForecastingModel(ABC):
    """Interfaz base para modelos de forecasting."""

    name: str = "base"
    display_name: str = "Base Forecasting"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.fc_config = config["forecasting"]
        self.model_config = config["forecasting"]["models"].get(self.name, {})
        self.horizon = self.fc_config.get("horizon_years", 5)
        self.freq = self.fc_config.get("freq", "YS")

    def run(self, df_ts: pd.DataFrame) -> pd.DataFrame:
        """
        Ejecuta el pipeline de forecasting para todos los países.

        Args:
            df_ts: DataFrame con columnas [Pais, ds, y].

        Returns:
            DataFrame con predicciones [Pais, ds, yhat, yhat_lower, yhat_upper].
        """
        logger.info(f"▶ {self.display_name}")

        countries = df_ts["Pais"].unique()
        logger.info(f"  Procesando {len(countries)} países...")

        all_forecasts = []

        for country in countries:
            try:
                country_data = df_ts[df_ts["Pais"] == country].sort_values("ds").copy()

                if len(country_data) < 3:
                    logger.warning(f"  {country}: datos insuficientes ({len(country_data)} puntos), omitido.")
                    continue

                forecast = self._train_country(country_data, country)

                if forecast is not None and len(forecast) > 0:
                    forecast["Pais"] = country
                    all_forecasts.append(forecast)

            except Exception as e:
                logger.warning(f"  {country}: error — {e}")
                continue

        if not all_forecasts:
            logger.error(f"  {self.display_name}: No se generaron predicciones.")
            return pd.DataFrame()

        df_forecast = pd.concat(all_forecasts, ignore_index=True)

        # Asegurar columnas estándar
        df_forecast = df_forecast[["Pais", "ds", "yhat", "yhat_lower", "yhat_upper"]]

        # Guardar Gold
        self._save_gold(df_forecast)

        logger.info(f"  Predicciones: {len(df_forecast)} puntos para {df_forecast['Pais'].nunique()} países")
        return df_forecast

    @abstractmethod
    def _train_country(self, df_country: pd.DataFrame, country: str) -> pd.DataFrame:
        """
        Entrena y predice para un solo país.

        Args:
            df_country: DataFrame con columnas [ds, y] para un país.
            country: Nombre del país.

        Returns:
            DataFrame con columnas [ds, yhat, yhat_lower, yhat_upper].
        """
        ...

    def _save_gold(self, df_forecast: pd.DataFrame) -> None:
        """Guarda predicciones en la capa Gold."""
        gold_dir = Path(self.config["paths"]["gold"]) / "forecasting" / self.name
        gold_dir.mkdir(parents=True, exist_ok=True)
        fmt = self.config["paths"].get("format", "parquet")

        path = gold_dir / f"predicciones.{fmt}"
        if fmt == "parquet":
            df_forecast.to_parquet(path, index=False, engine="pyarrow")
        else:
            df_forecast.to_csv(path, index=False, encoding="utf-8")

        logger.info(f"  Gold → {self.name}/predicciones.{fmt}")
