"""Registro de modelos de forecasting."""

from forecasting.prophet_model import ProphetModel
from forecasting.neuralprophet_model import NeuralProphetModel
from forecasting.statsforecast_model import StatsForecastModel
from forecasting.timesfm_model import TimesFMModel

FORECASTING_MODELS = {
    "prophet": ProphetModel,
    "neuralprophet": NeuralProphetModel,
    "statsforecast": StatsForecastModel,
    "timesfm": TimesFMModel,
}


def get_enabled_models(config):
    """Retorna solo los modelos de forecasting habilitados."""
    enabled = {}
    for name, cls in FORECASTING_MODELS.items():
        model_cfg = config["forecasting"]["models"].get(name, {})
        if model_cfg.get("enabled", False):
            enabled[name] = cls
    return enabled
