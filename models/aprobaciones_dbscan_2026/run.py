"""
Main Entry Point for the BCIE DBSCAN Clustering Model (2026).

This script orchestrates the end-to-end execution of the analytics pipeline:
1. ETL: Data extraction from CKAN and preprocessing.
2. Training: DBSCAN clustering with grid search optimization.
3. Dashboard: Generation of the interactive HTML dashboard.

Usage:
    python run.py
    python run.py --skip-etl
    python run.py --optimize

Dependencies:
    - config/local.yaml
    - src/pipelines/
    - src/dashboard/
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DBSCAN_Pipeline")


def main():
    """
    Delegates execution to the entrypoint orchestrator.
    This ensures consistency whether running via run.py or entrypoint/main.py.
    """
    # Import and delegate to the canonical entrypoint
    try:
        from entrypoint.main import main as entrypoint_main
        entrypoint_main()
    except ImportError as e:
        logger.error(f"Could not import entrypoint: {e}")
        logger.info("Attempting direct pipeline execution...")

        # Fallback: run pipeline directly
        config_path = "config/local.yaml"
        run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")

        logger.info(f">>> INITIATING BCIE DBSCAN CLUSTERING PIPELINE (Run ID: {run_id}) <<<")

        # 1. ETL
        logger.info("--- PHASE 1: ETL ---")
        try:
            from src.pipelines.etl_pipeline import run_etl
            run_etl(config_path, run_id=run_id)
        except Exception as ex:
            logger.error(f"ETL Failed: {ex}")
            return

        # 2. Training
        logger.info("--- PHASE 2: TRAINING (DBSCAN) ---")
        try:
            from src.pipelines.training_pipeline import train_dbscan
            train_dbscan(config_path, run_id=run_id)
        except Exception as ex:
            logger.error(f"Training Failed: {ex}")
            return

        # 3. Dashboard
        logger.info("--- PHASE 3: DASHBOARD ---")
        try:
            from src.dashboard.generate_dashboard import generate_dashboard
            generate_dashboard(config_path, run_id=run_id)
        except Exception as ex:
            logger.error(f"Dashboard Failed: {ex}")

        logger.info(">>> PIPELINE COMPLETED SUCCESSFULLY <<<")


if __name__ == "__main__":
    main()
