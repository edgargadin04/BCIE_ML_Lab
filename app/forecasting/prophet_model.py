"""Modelo Prophet (Facebook/Meta)."""

import pandas as pd
from forecasting.base import ForecastingModel
from core.logger import get_logger

logger = get_logger(__name__)


class ProphetModel(ForecastingModel):
    name = "prophet"
    display_name = "Prophet"

    def _train_country(self, df_country, country):
        from prophet import Prophet
        import logging
        logging.getLogger("prophet").setLevel(logging.WARNING)
        logging.getLogger("cmdstanpy").setLevel(logging.WARNING)

        mode = self.model_config.get("seasonality_mode", "multiplicative")

        model = Prophet(
            seasonality_mode=mode,
            yearly_seasonality=self.model_config.get("yearly_seasonality", False),
        )

        model.fit(df_country[["ds", "y"]])

        future = model.make_future_dataframe(periods=self.horizon, freq=self.freq)
        forecast = model.predict(future)

        # Solo futuro
        last_date = df_country["ds"].max()
        forecast = forecast[forecast["ds"] > last_date]

        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
