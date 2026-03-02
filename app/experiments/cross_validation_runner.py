"""
══════════════════════════════════════════════════════════════
Cross-Validation Runner for Forecasting Models
Runs TimeSeriesSplit with K=3..8 folds for each model.
Outputs: data/gold/experiments/cross_validation_results.json
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

logger = get_logger("CrossValidation")


def mape(y_true, y_pred):
    """Mean Absolute Percentage Error."""
    y_true, y_pred = np.array(y_true, dtype=float), np.array(y_pred, dtype=float)
    mask = y_true != 0
    if mask.sum() == 0:
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def rmse(y_true, y_pred):
    """Root Mean Squared Error."""
    return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred)) ** 2))


def mae(y_true, y_pred):
    """Mean Absolute Error."""
    return np.mean(np.abs(np.array(y_true) - np.array(y_pred)))


def run_prophet_cv(df_ts, country_data, n_splits):
    """Cross-validate Prophet for one country."""
    from prophet import Prophet
    import logging
    logging.getLogger("prophet").setLevel(logging.ERROR)
    logging.getLogger("cmdstanpy").setLevel(logging.ERROR)

    n = len(country_data)
    min_train = max(3, n // 3)
    fold_size = max(1, (n - min_train) // n_splits)

    mapes, rmses = [], []
    for fold in range(n_splits):
        train_end = min_train + fold * fold_size
        if train_end >= n:
            break
        test_end = min(train_end + fold_size, n)

        train = country_data.iloc[:train_end]
        test = country_data.iloc[train_end:test_end]

        if len(test) == 0:
            continue

        model = Prophet(yearly_seasonality=False, seasonality_mode="multiplicative")
        model.fit(train[["ds", "y"]])

        future = pd.DataFrame({"ds": test["ds"]})
        pred = model.predict(future)

        m = mape(test["y"].values, pred["yhat"].values)
        r = rmse(test["y"].values, pred["yhat"].values)
        if not np.isnan(m):
            mapes.append(m)
        rmses.append(r)

    return np.mean(mapes) if mapes else np.nan, np.mean(rmses) if rmses else np.nan


def run_neuralprophet_cv(df_ts, country_data, n_splits):
    """Cross-validate NeuralProphet for one country."""
    from neuralprophet import NeuralProphet, set_log_level
    set_log_level("ERROR")

    n = len(country_data)
    min_train = max(3, n // 3)
    fold_size = max(1, (n - min_train) // n_splits)

    mapes, rmses = [], []
    for fold in range(n_splits):
        train_end = min_train + fold * fold_size
        if train_end >= n:
            break
        test_end = min(train_end + fold_size, n)

        train = country_data.iloc[:train_end]
        test = country_data.iloc[train_end:test_end]

        if len(test) == 0:
            continue

        model = NeuralProphet(epochs=50, learning_rate=0.1, yearly_seasonality=False)
        model.fit(train[["ds", "y"]], freq="YS")

        future = model.make_future_dataframe(train[["ds", "y"]], periods=len(test))
        pred = model.predict(future)
        pred = pred.tail(len(test))

        m = mape(test["y"].values, pred["yhat1"].values)
        r = rmse(test["y"].values, pred["yhat1"].values)
        if not np.isnan(m):
            mapes.append(m)
        rmses.append(r)

    return np.mean(mapes) if mapes else np.nan, np.mean(rmses) if rmses else np.nan


def run_statsforecast_cv(df_ts, country_data, n_splits):
    """Cross-validate StatsForecast for one country."""
    from statsforecast import StatsForecast
    from statsforecast.models import AutoARIMA

    n = len(country_data)
    min_train = max(3, n // 3)
    fold_size = max(1, (n - min_train) // n_splits)

    mapes, rmses = [], []
    for fold in range(n_splits):
        train_end = min_train + fold * fold_size
        if train_end >= n:
            break
        test_end = min(train_end + fold_size, n)

        train = country_data.iloc[:train_end].copy()
        test = country_data.iloc[train_end:test_end].copy()

        if len(test) == 0:
            continue

        # StatsForecast requires columns: unique_id, ds, y (in that order)
        train_sf = pd.DataFrame({
            "unique_id": "country",
            "ds": pd.to_datetime(train["ds"]),
            "y": train["y"].astype(float),
        })

        try:
            sf = StatsForecast(
                models=[AutoARIMA(season_length=1)],
                freq="YS", n_jobs=1
            )
            sf.fit(train_sf)
            pred = sf.predict(h=len(test))
            y_pred = pred["AutoARIMA"].values

            m = mape(test["y"].values.astype(float), y_pred)
            r = rmse(test["y"].values.astype(float), y_pred)
            if not np.isnan(m):
                mapes.append(m)
            rmses.append(r)
        except Exception as e:
            logger.warning(f"    SF fold error: {type(e).__name__}: {e}")
            continue

    return np.mean(mapes) if mapes else np.nan, np.mean(rmses) if rmses else np.nan


def run_cv_experiment(config):
    """Run cross-validation for all models across 3-8 folds."""
    fmt = config["paths"].get("format", "parquet")
    silver_dir = Path(config["paths"]["silver"])
    fc_path = silver_dir / f"aprobaciones_forecasting.{fmt}"

    if fmt == "parquet":
        df = pd.read_parquet(fc_path)
    else:
        df = pd.read_csv(fc_path)

    df["ds"] = pd.to_datetime(df["ds"])

    # Use top 5 countries by data points for CV (speed)
    top_countries = df.groupby("Pais").size().nlargest(5).index.tolist()
    logger.info(f"CV countries: {top_countries}")

    model_runners = {
        "Prophet": run_prophet_cv,
        "NeuralProphet": run_neuralprophet_cv,
        "StatsForecast": run_statsforecast_cv,
    }

    results = {}

    for n_folds in range(3, 9):
        logger.info(f"━━━ K = {n_folds} folds ━━━")
        fold_results = {}

        for model_name, runner in model_runners.items():
            logger.info(f"  {model_name}...")
            country_mapes = []
            country_rmses = []

            for country in top_countries:
                cdata = df[df["Pais"] == country].sort_values("ds").copy()
                if len(cdata) < 5:
                    continue
                try:
                    m, r = runner(df, cdata, n_folds)
                    if not np.isnan(m):
                        country_mapes.append(m)
                    if not np.isnan(r):
                        country_rmses.append(r)
                except Exception as e:
                    logger.warning(f"    {country}: {e}")
                    continue

            avg_mape = float(np.mean(country_mapes)) if country_mapes else None
            avg_rmse = float(np.mean(country_rmses)) if country_rmses else None

            fold_results[model_name] = {
                "mape": round(avg_mape, 2) if avg_mape else None,
                "rmse": round(avg_rmse, 2) if avg_rmse else None,
                "countries_evaluated": len(country_mapes),
            }
            logger.info(f"    MAPE={avg_mape:.2f}%, RMSE={avg_rmse:.2f}" if avg_mape else f"    N/A")

        results[f"{n_folds}_folds"] = fold_results

    # Add TimesFM placeholder (no easy CV without GPU)
    for k in results:
        results[k]["TimesFM"] = {"mape": None, "rmse": None, "countries_evaluated": 0, "note": "Requires GPU"}

    # Save results
    out_dir = Path(config["paths"]["gold"]) / "experiments"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "cross_validation_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Results saved → {out_path}")
    return results


if __name__ == "__main__":
    config = load_config()
    results = run_cv_experiment(config)
    print(json.dumps(results, indent=2))
