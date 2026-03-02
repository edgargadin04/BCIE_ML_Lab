"""Modelo NeuralProphet — optimizado con autoregresión y LR bajo."""

import pandas as pd
import numpy as np
from forecasting.base import ForecastingModel
from core.logger import get_logger

logger = get_logger(__name__)


class NeuralProphetModel(ForecastingModel):
    name = "neuralprophet"
    display_name = "NeuralProphet"

    def _train_country(self, df_country, country):
        from neuralprophet import NeuralProphet, set_log_level
        set_log_level("ERROR")

        epochs = self.model_config.get("epochs", 60)
        lr = self.model_config.get("learning_rate", 0.01)
        quantiles = self.model_config.get("quantiles", [0.05, 0.95])
        n_lags = self.model_config.get("n_lags", 3)
        batch_size = self.model_config.get("batch_size", 32)

        model = NeuralProphet(
            n_forecasts=self.horizon,
            n_lags=n_lags,
            epochs=epochs,
            learning_rate=lr,
            batch_size=batch_size,
            quantiles=quantiles,
        )

        model.fit(df_country[["ds", "y"]], freq=self.freq)
        future = model.make_future_dataframe(df_country[["ds", "y"]], periods=self.horizon)
        forecast = model.predict(future)

        # Extraer predicciones y quantiles
        last_date = df_country["ds"].max()
        forecast = forecast[forecast["ds"] > last_date].head(self.horizon)

        # NeuralProphet nombra las cols como yhat1, yhat1 5.0%, yhat1 95.0%
        yhat_cols = [c for c in forecast.columns if c.startswith("yhat") and "%" not in c]
        lower_cols = [c for c in forecast.columns if "5.0%" in c]
        upper_cols = [c for c in forecast.columns if "95.0%" in c]

        result = pd.DataFrame({"ds": forecast["ds"].values})

        if yhat_cols:
            result["yhat"] = forecast[yhat_cols].mean(axis=1).values
        if lower_cols:
            result["yhat_lower"] = forecast[lower_cols].mean(axis=1).values
        else:
            result["yhat_lower"] = result["yhat"] * 0.8
        if upper_cols:
            result["yhat_upper"] = forecast[upper_cols].mean(axis=1).values
        else:
            result["yhat_upper"] = result["yhat"] * 1.2

        return result
