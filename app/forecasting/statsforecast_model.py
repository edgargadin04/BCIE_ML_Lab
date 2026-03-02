"""Modelo StatsForecast (Ensemble AutoARIMA + Theta)."""

import pandas as pd
import numpy as np
from forecasting.base import ForecastingModel
from core.logger import get_logger

logger = get_logger(__name__)


class StatsForecastModel(ForecastingModel):
    name = "statsforecast"
    display_name = "StatsForecast (AutoARIMA + Theta)"

    def _train_country(self, df_country, country):
        from statsforecast import StatsForecast
        from statsforecast.models import AutoARIMA, DynamicOptimizedTheta

        # Preparar formato StatsForecast
        sf_df = df_country[["ds", "y"]].copy()
        sf_df["unique_id"] = country
        sf_df = sf_df[["unique_id", "ds", "y"]]

        models = [
            AutoARIMA(season_length=1),
            DynamicOptimizedTheta(season_length=1),
        ]

        sf = StatsForecast(models=models, freq="YS", n_jobs=1)
        sf.fit(sf_df)
        forecast = sf.predict(h=self.horizon, level=[95])

        # Ensemble: promedio de ambos modelos
        arima_col = [c for c in forecast.columns if "AutoARIMA" in c and "lo" not in c and "hi" not in c]
        theta_col = [c for c in forecast.columns if "Theta" in c and "lo" not in c and "hi" not in c]

        yhat_arima = forecast[arima_col[0]].values if arima_col else np.zeros(self.horizon)
        yhat_theta = forecast[theta_col[0]].values if theta_col else np.zeros(self.horizon)

        yhat = (yhat_arima + yhat_theta) / 2

        # Intervalos de confianza
        lo_cols = [c for c in forecast.columns if "lo" in c]
        hi_cols = [c for c in forecast.columns if "hi" in c]

        if lo_cols:
            yhat_lower = forecast[lo_cols].mean(axis=1).values
        else:
            yhat_lower = yhat * 0.8

        if hi_cols:
            yhat_upper = forecast[hi_cols].mean(axis=1).values
        else:
            yhat_upper = yhat * 1.2

        result = pd.DataFrame({
            "ds": forecast.index if "ds" not in forecast.columns else forecast["ds"],
            "yhat": yhat,
            "yhat_lower": yhat_lower,
            "yhat_upper": yhat_upper,
        })

        # Asegurar que ds sea datetime
        if not hasattr(result["ds"].iloc[0], "year"):
            result["ds"] = pd.to_datetime(result["ds"])

        return result
