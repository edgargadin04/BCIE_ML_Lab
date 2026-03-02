"""
═══════════════════════════════════════════════════════════
NeuralProphet-Only Experiment Runner
Re-runs ONLY NeuralProphet for partitions + cross-validation
and patches existing JSON results without touching other models.
═══════════════════════════════════════════════════════════
"""

import sys, os, json, warnings
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import TimeSeriesSplit

# Setup paths
APP_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(APP_DIR))
os.chdir(APP_DIR)

warnings.filterwarnings("ignore")

from core.config import load_config
from core.logger import get_logger

logger = get_logger("NeuralProphet-Repair")

# ── GPU detection ──
import torch
USE_GPU = torch.cuda.is_available()
ACCELERATOR = "gpu" if USE_GPU else "cpu"
logger.info(f"Device: {ACCELERATOR} ({'CUDA: ' + torch.cuda.get_device_name(0) if USE_GPU else 'CPU'})")


def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true, dtype=float), np.array(y_pred, dtype=float)
    mask = y_true != 0
    if mask.sum() == 0:
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred)) ** 2))


def run_neuralprophet_partition(train, test):
    from neuralprophet import NeuralProphet, set_log_level
    set_log_level("ERROR")

    # Use pure trend mode (no n_lags) so we can predict the full test horizon
    model = NeuralProphet(
        epochs=60, learning_rate=0.01,
        yearly_seasonality=False, batch_size=32,
        accelerator=ACCELERATOR,
    )
    model.fit(train[["ds", "y"]], freq="YS")
    future = model.make_future_dataframe(train[["ds", "y"]], periods=len(test))
    pred = model.predict(future)
    # Filter to only future dates
    last_train_date = train["ds"].max()
    future_pred = pred[pred["ds"] > last_train_date]
    result = future_pred["yhat1"].dropna().values
    return result


def run_neuralprophet_cv_fold(train, test):
    """Run NeuralProphet on a single CV fold."""
    from neuralprophet import NeuralProphet, set_log_level
    set_log_level("ERROR")

    # Use pure trend mode (no n_lags) for multi-step prediction
    model = NeuralProphet(
        epochs=60, learning_rate=0.01,
        yearly_seasonality=False, batch_size=32,
        accelerator=ACCELERATOR,
    )
    model.fit(train[["ds", "y"]], freq="YS")
    future = model.make_future_dataframe(train[["ds", "y"]], periods=len(test))
    pred = model.predict(future)
    last_train_date = train["ds"].max()
    future_pred = pred[pred["ds"] > last_train_date]
    result = future_pred["yhat1"].dropna().values
    return result


def main():
    config = load_config()
    fmt = config["paths"].get("format", "parquet")
    silver_dir = Path(config["paths"]["silver"])
    gold_dir = Path(config["paths"]["gold"])
    fc_path = silver_dir / f"aprobaciones_forecasting.{fmt}"

    if fmt == "parquet":
        df = pd.read_parquet(fc_path)
    else:
        df = pd.read_csv(fc_path)

    df["ds"] = pd.to_datetime(df["ds"])

    top_countries = df.groupby("Pais").size().nlargest(5).index.tolist()
    logger.info(f"Countries: {top_countries}")

    # ═══ PART 1: Partition Experiment ═══
    logger.info("═══ PARTITION EXPERIMENTS ═══")
    
    part_path = gold_dir / "experiments" / "partition_results.json"
    with open(part_path, "r", encoding="utf-8") as f:
        part_results = json.load(f)

    partitions = list(range(60, 100, 5))
    
    for train_pct in partitions:
        test_pct = 100 - train_pct
        key = f"{train_pct}/{test_pct}"
        logger.info(f"━━━ Partition {key} ━━━")
        
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
            test_data = cdata.iloc[split_idx:]

            if len(test_data) == 0:
                continue

            try:
                y_pred = run_neuralprophet_partition(train, test_data)
                y_true = test_data["y"].values

                min_len = min(len(y_true), len(y_pred))
                y_true = y_true[:min_len]
                y_pred = y_pred[:min_len]

                m = mape(y_true, y_pred)
                r = rmse(y_true, y_pred)
                if not np.isnan(m):
                    country_mapes.append(m)
                if not np.isnan(r):
                    country_rmses.append(r)
                logger.info(f"    {country}: MAPE={m:.2f}%")
            except Exception as e:
                logger.warning(f"    {country}: ERROR - {e}")
                continue

        avg_mape = float(np.mean(country_mapes)) if country_mapes else None
        avg_rmse = float(np.mean(country_rmses)) if country_rmses else None

        part_results[key]["NeuralProphet"] = {
            "mape": round(avg_mape, 2) if avg_mape else None,
            "rmse": round(avg_rmse, 2) if avg_rmse else None,
            "countries_evaluated": len(country_mapes),
        }
        logger.info(f"  NeuralProphet {key}: MAPE={avg_mape:.2f}%, countries={len(country_mapes)}" if avg_mape else f"  NeuralProphet {key}: N/A")

    with open(part_path, "w", encoding="utf-8") as f:
        json.dump(part_results, f, indent=2, ensure_ascii=False)
    logger.info(f"Partition results updated → {part_path}")

    # ═══ PART 2: Cross-Validation ═══
    logger.info("═══ CROSS-VALIDATION ═══")
    
    cv_path = gold_dir / "experiments" / "cross_validation_results.json"
    with open(cv_path, "r", encoding="utf-8") as f:
        cv_results = json.load(f)

    for n_splits in range(3, 9):
        key = f"{n_splits}_folds"
        logger.info(f"━━━ {n_splits}-Fold CV ━━━")
        
        country_mapes = []
        country_rmses = []

        for country in top_countries:
            cdata = df[df["Pais"] == country].sort_values("ds").copy().reset_index(drop=True)
            n = len(cdata)
            if n < n_splits + 2:
                continue

            tscv = TimeSeriesSplit(n_splits=n_splits)
            fold_mapes = []

            for fold_i, (train_idx, test_idx) in enumerate(tscv.split(cdata)):
                train = cdata.iloc[train_idx]
                test_data = cdata.iloc[test_idx]

                if len(train) < 3 or len(test_data) == 0:
                    continue

                try:
                    y_pred = run_neuralprophet_cv_fold(train, test_data)
                    y_true = test_data["y"].values

                    min_len = min(len(y_true), len(y_pred))
                    y_true = y_true[:min_len]
                    y_pred = y_pred[:min_len]

                    m = mape(y_true, y_pred)
                    if not np.isnan(m):
                        fold_mapes.append(m)
                except Exception as e:
                    logger.warning(f"    {country} fold-{fold_i}: {e}")
                    continue

            if fold_mapes:
                avg_country_mape = float(np.mean(fold_mapes))
                country_mapes.append(avg_country_mape)
                logger.info(f"    {country}: avg MAPE={avg_country_mape:.2f}% ({len(fold_mapes)} folds)")

        avg_mape = float(np.mean(country_mapes)) if country_mapes else None

        cv_results[key]["NeuralProphet"] = {
            "mape": round(avg_mape, 2) if avg_mape else None,
            "rmse": None,
            "countries_evaluated": len(country_mapes),
        }
        logger.info(f"  NeuralProphet {key}: MAPE={avg_mape:.2f}%, countries={len(country_mapes)}" if avg_mape else f"  NeuralProphet {key}: N/A")

    with open(cv_path, "w", encoding="utf-8") as f:
        json.dump(cv_results, f, indent=2, ensure_ascii=False)
    logger.info(f"CV results updated → {cv_path}")

    logger.info("═══ DONE ═══")


if __name__ == "__main__":
    main()
