"""Modelo TimesFM 2.5 (Google Foundation Model) — PyTorch + CUDA."""

import pandas as pd
import numpy as np
from forecasting.base import ForecastingModel
from core.logger import get_logger

logger = get_logger(__name__)


class TimesFMModel(ForecastingModel):
    name = "timesfm"
    display_name = "TimesFM (Google)"

    def _load_model(self):
        """Load and compile TimesFM model (cached across countries)."""
        if hasattr(self, "_tfm") and self._tfm is not None:
            return

        import torch
        import timesfm

        device = "cuda" if torch.cuda.is_available() else "cpu"
        repo_id = self.model_config.get(
            "repo_id", "google/timesfm-2.5-200m-pytorch"
        )

        logger.info(f"  Cargando TimesFM: {repo_id} en {device}...")
        self._tfm = timesfm.TimesFM_2p5_200M_torch.from_pretrained(repo_id)

        # Compile with forecast config
        config = timesfm.ForecastConfig(
            max_context=512,
            max_horizon=self.horizon * 2,
        )
        self._tfm.compile(config)
        self._device = device

        mem = torch.cuda.memory_allocated() / 1e6 if device == "cuda" else 0
        logger.info(f"  TimesFM listo — GPU memory: {mem:.0f}MB")

    def _train_country(self, df_country, country):
        import torch

        self._load_model()

        history = df_country["y"].values.astype(np.float64)

        with torch.no_grad():
            point_forecast, quantiles = self._tfm.forecast(
                horizon=self.horizon,
                inputs=[history],
            )

        forecast_values = point_forecast[0][: self.horizon]

        last_year = df_country["ds"].max().year
        future_dates = [
            pd.Timestamp(year=last_year + i + 1, month=1, day=1)
            for i in range(len(forecast_values))
        ]

        # Confidence intervals from quantiles if available
        if quantiles is not None and len(quantiles) > 0:
            q_arr = quantiles[0]  # shape: (horizon, n_quantiles)
            if q_arr.ndim == 2 and q_arr.shape[1] >= 2:
                lower = np.maximum(q_arr[:, 0], 0)
                upper = q_arr[:, -1]
            else:
                cv = 0.15
                lower = np.maximum(forecast_values - 1.96 * np.abs(forecast_values) * cv, 0)
                upper = forecast_values + 1.96 * np.abs(forecast_values) * cv
        else:
            cv = 0.15
            lower = np.maximum(forecast_values - 1.96 * np.abs(forecast_values) * cv, 0)
            upper = forecast_values + 1.96 * np.abs(forecast_values) * cv

        return pd.DataFrame({
            "ds": future_dates,
            "yhat": forecast_values,
            "yhat_lower": lower[: len(forecast_values)],
            "yhat_upper": upper[: len(forecast_values)],
        })
