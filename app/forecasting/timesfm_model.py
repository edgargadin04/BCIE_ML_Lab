"""Modelo TimesFM (Google Foundation Model)."""

import pandas as pd
import numpy as np
from forecasting.base import ForecastingModel
from core.logger import get_logger

logger = get_logger(__name__)


class TimesFMModel(ForecastingModel):
    name = "timesfm"
    display_name = "TimesFM (Google)"

    def _train_country(self, df_country, country):
        import torch
        from transformers.models.timesfm.modeling_timesfm import TimesFmModelForPrediction

        repo_id = self.model_config.get("repo_id", "google/timesfm-2.0-500m-pytorch")
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Cargar modelo (cacheado globalmente)
        if not hasattr(self, "_model"):
            logger.info(f"  Cargando TimesFM: {repo_id} en {device}...")
            self._model = TimesFmModelForPrediction.from_pretrained(
                repo_id, trust_remote_code=True, device_map=device,
            )
            self._device = device

        history = df_country["y"].values
        input_tensor = torch.tensor(history, dtype=torch.float32).unsqueeze(0).to(self._device)
        freq_tensor = torch.tensor([0]).to(self._device)

        with torch.no_grad():
            outputs = self._model(past_values=input_tensor, freq=freq_tensor)
            forecast_values = outputs.mean_predictions.cpu().numpy().squeeze()

        if len(forecast_values) > self.horizon:
            forecast_values = forecast_values[-self.horizon:]

        last_year = df_country["ds"].max().year
        future_dates = [pd.Timestamp(year=last_year + i + 1, month=1, day=1)
                        for i in range(len(forecast_values))]

        # Intervalos de confianza (estimación proporcional)
        cv = 0.15
        lower = np.maximum(forecast_values - 1.96 * np.abs(forecast_values) * cv, 0)
        upper = forecast_values + 1.96 * np.abs(forecast_values) * cv

        return pd.DataFrame({
            "ds": future_dates,
            "yhat": forecast_values,
            "yhat_lower": lower,
            "yhat_upper": upper,
        })
