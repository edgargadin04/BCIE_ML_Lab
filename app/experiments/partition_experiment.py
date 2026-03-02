"""
══════════════════════════════════════════════════════════════
Partition Experiment Runner
Tests train/test splits from 60/40 to 95/5 in 5% increments.
Outputs: data/gold/experiments/partition_results.json
══════════════════════════════════════════════════════════════
"""

import sys, os, json, warnings
import numpy as np
import pandas as pd
from pathlib import Path

# Setup paths
APP_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(APP_DIR))
os.chdir(APP_DIR)

warnings.filterwarnings("ignore")

from core.config import load_config
from core.logger import get_logger

logger = get_logger("PartitionExperiment")


def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true, dtype=float), np.array(y_pred, dtype=float)
    mask = y_true != 0
    if mask.sum() == 0:
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred)) ** 2))


def run_prophet_partition(train, test):
    from prophet import Prophet
    import logging
    logging.getLogger("prophet").setLevel(logging.ERROR)
    logging.getLogger("cmdstanpy").setLevel(logging.ERROR)

    model = Prophet(yearly_seasonality=False, seasonality_mode="multiplicative")
    model.fit(train[["ds", "y"]])
    future = pd.DataFrame({"ds": test["ds"]})
    pred = model.predict(future)
    return pred["yhat"].values


def run_neuralprophet_partition(train, test):
    from neuralprophet import NeuralProphet, set_log_level
    set_log_level("ERROR")

    model = NeuralProphet(epochs=50, learning_rate=0.1, yearly_seasonality=False)
    model.fit(train[["ds", "y"]], freq="YS")
    future = model.make_future_dataframe(train[["ds", "y"]], periods=len(test))
    pred = model.predict(future)
    return pred["yhat1"].tail(len(test)).values


def run_statsforecast_partition(train, test):
    from statsforecast import StatsForecast
    from statsforecast.models import AutoARIMA

    # Create clean DataFrame with only required columns
    train_sf = pd.DataFrame({
        "unique_id": "country",
        "ds": pd.to_datetime(train["ds"]),
        "y": train["y"].astype(float),
    })

    sf = StatsForecast(
        models=[AutoARIMA(season_length=1)],
        freq="YS", n_jobs=1
    )
    sf.fit(train_sf)
    pred = sf.predict(h=len(test))
    return pred["AutoARIMA"].values


# ── TimesFM model (loaded once, shared across partitions) ──
_timesfm_model = None

def _get_timesfm():
    global _timesfm_model
    if _timesfm_model is None:
        import torch, timesfm
        logger.info("    Loading TimesFM 2.5 on GPU...")
        _timesfm_model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
            "google/timesfm-2.5-200m-pytorch"
        )
        fc_config = timesfm.ForecastConfig(max_context=512, max_horizon=128)
        _timesfm_model.compile(fc_config)
        logger.info(f"    GPU memory: {torch.cuda.memory_allocated()/1e6:.0f}MB")
    return _timesfm_model


def run_timesfm_partition(train, test):
    import torch
    tfm = _get_timesfm()
    history = train["y"].values.astype(np.float64)
    with torch.no_grad():
        pf, _ = tfm.forecast(horizon=len(test), inputs=[history])
    return pf[0][:len(test)]


def run_partition_experiment(config):
    """Run partition experiments from 60/40 to 95/5."""
    fmt = config["paths"].get("format", "parquet")
    silver_dir = Path(config["paths"]["silver"])
    fc_path = silver_dir / f"aprobaciones_forecasting.{fmt}"

    if fmt == "parquet":
        df = pd.read_parquet(fc_path)
    else:
        df = pd.read_csv(fc_path)

    df["ds"] = pd.to_datetime(df["ds"])

    # Use top 5 countries
    top_countries = df.groupby("Pais").size().nlargest(5).index.tolist()
    logger.info(f"Partition countries: {top_countries}")

    model_runners = {
        "Prophet": run_prophet_partition,
        "NeuralProphet": run_neuralprophet_partition,
        "StatsForecast": run_statsforecast_partition,
        "TimesFM": run_timesfm_partition,
    }

    partitions = list(range(60, 100, 5))  # 60, 65, 70, ..., 95
    results = {}

    for train_pct in partitions:
        test_pct = 100 - train_pct
        key = f"{train_pct}/{test_pct}"
        logger.info(f"━━━ Partition {key} ━━━")
        partition_results = {}

        for model_name, runner in model_runners.items():
            logger.info(f"  {model_name}...")
            country_mapes = []
            country_rmses = []

            for country in top_countries:
                cdata = df[df["Pais"] == country].sort_values("ds").copy()
                n = len(cdata)
                if n < 5:
                    continue

                split_idx = int(n * train_pct / 100)
                if split_idx < 3 or split_idx >= n:
                    continue

                train = cdata.iloc[:split_idx]
                test = cdata.iloc[split_idx:]

                if len(test) == 0:
                    continue

                try:
                    y_pred = runner(train, test)
                    y_true = test["y"].values

                    # Align lengths
                    min_len = min(len(y_true), len(y_pred))
                    y_true = y_true[:min_len]
                    y_pred = y_pred[:min_len]

                    m = mape(y_true, y_pred)
                    r = rmse(y_true, y_pred)
                    if not np.isnan(m):
                        country_mapes.append(m)
                    if not np.isnan(r):
                        country_rmses.append(r)
                except Exception as e:
                    logger.warning(f"    {country}: {e}")
                    continue

            avg_mape = float(np.mean(country_mapes)) if country_mapes else None
            avg_rmse = float(np.mean(country_rmses)) if country_rmses else None

            partition_results[model_name] = {
                "mape": round(avg_mape, 2) if avg_mape else None,
                "rmse": round(avg_rmse, 2) if avg_rmse else None,
                "countries_evaluated": len(country_mapes),
            }
            logger.info(f"    MAPE={avg_mape:.2f}%, RMSE={avg_rmse:.2f}" if avg_mape else f"    N/A")


        results[key] = partition_results

    # Save results
    out_dir = Path(config["paths"]["gold"]) / "experiments"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "partition_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Results saved → {out_path}")
    return results


if __name__ == "__main__":
    config = load_config()
    results = run_partition_experiment(config)
    print(json.dumps(results, indent=2))
