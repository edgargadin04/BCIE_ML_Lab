"""
╔══════════════════════════════════════════════════════════════╗
║  BCIE Datos Abiertos — Pipeline Unificado de Producción     ║
║  Versión 2.0.0                                               ║
║  Arquitectura Medallón: Bronze → Silver → Gold               ║
╚══════════════════════════════════════════════════════════════╝

Punto de entrada único para todo el pipeline de analítica avanzada.

Uso:
    python main.py                        # Ejecutar todo
    python main.py --mode clustering      # Solo clustering
    python main.py --mode forecasting     # Solo forecasting
    python main.py --mode dashboard       # Solo dashboard
    python main.py --model kmeans         # Un modelo específico
    python main.py --skip-etl             # Saltar extracción (usar caché)
"""

import argparse
import sys
import json
import time
from pathlib import Path

# Asegurar que el directorio de la app esté en el path
sys.path.insert(0, str(Path(__file__).parent))

from core.logger import get_logger
from core.config import load_config
from core.etl import run_bronze
from core.preprocessing import run_silver

logger = get_logger("BCIE_Pipeline")


def run_clustering(df_clustering, config, model_filter=None):
    """Ejecuta todos los modelos de clustering habilitados."""
    from clustering import get_enabled_models

    models = get_enabled_models(config)
    results = {}

    if model_filter:
        models = {k: v for k, v in models.items() if k == model_filter}
        if not models:
            logger.error(f"Modelo '{model_filter}' no encontrado o no habilitado.")
            return results

    logger.info(f"━━━ CAPA GOLD: CLUSTERING ({len(models)} modelos) ━━━")

    for name, model_cls in models.items():
        try:
            model = model_cls(config)
            df_result, metrics = model.run(df_clustering)
            results[name] = {"data": df_result, "metrics": metrics}
        except Exception as e:
            logger.error(f"  {name}: FALLO — {e}")
            continue

    # Guardar tabla comparativa de métricas
    _save_comparison_table(results, config, "clustering")

    return results


def run_forecasting(df_forecasting, config, model_filter=None):
    """Ejecuta todos los modelos de forecasting habilitados."""
    from forecasting import get_enabled_models

    models = get_enabled_models(config)
    results = {}

    if model_filter:
        models = {k: v for k, v in models.items() if k == model_filter}
        if not models:
            logger.error(f"Modelo '{model_filter}' no encontrado o no habilitado.")
            return results

    logger.info(f"━━━ CAPA GOLD: FORECASTING ({len(models)} modelos) ━━━")

    for name, model_cls in models.items():
        try:
            model = model_cls(config)
            df_forecast = model.run(df_forecasting)
            results[name] = {"data": df_forecast}
        except Exception as e:
            logger.error(f"  {name}: FALLO — {e}")
            continue

    # Guardar tabla comparativa
    _save_comparison_table(results, config, "forecasting")

    return results


def _save_comparison_table(results, config, model_type):
    """Guarda tabla comparativa de métricas en Gold."""
    gold_dir = Path(config["paths"]["gold"])
    fmt = config["paths"].get("format", "parquet")

    if model_type == "clustering":
        comparisons = []
        for name, res in results.items():
            m = res.get("metrics", {})
            comparisons.append({
                "modelo": name,
                "k": m.get("k"),
                "silhouette": m.get("silhouette"),
                "davies_bouldin": m.get("davies_bouldin"),
                "calinski_harabasz": m.get("calinski_harabasz"),
                "stability_ari": m.get("stability_ari"),
                "neg_silhouette_pct": m.get("neg_silhouette_pct"),
                "size_cv": m.get("size_cv"),
            })

        if comparisons:
            import pandas as pd
            df_comp = pd.DataFrame(comparisons)
            path = gold_dir / f"comparativa_clustering.{fmt}"
            if fmt == "parquet":
                df_comp.to_parquet(path, index=False, engine="pyarrow")
            else:
                df_comp.to_csv(path, index=False)
            logger.info(f"  Comparativa clustering → {path.name}")


def run_dashboard(config, clustering_results=None, forecasting_results=None):
    """Genera el dashboard unificado."""
    logger.info("━━━ DASHBOARD UNIFICADO ━━━")
    from dashboard.generator import generate_unified_dashboard
    generate_unified_dashboard(config, clustering_results, forecasting_results)


def main():
    parser = argparse.ArgumentParser(
        description="BCIE Datos Abiertos — Pipeline de Analítica Avanzada",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["all", "etl", "clustering", "forecasting", "dashboard"],
        default="all",
        help="Modo de ejecución (default: all)",
    )
    parser.add_argument("--model", type=str, help="Ejecutar un modelo específico (ej: kmeans, prophet)")
    parser.add_argument("--skip-etl", action="store_true", help="Saltar ETL, usar datos existentes en Silver")
    parser.add_argument("--config", type=str, default=None, help="Ruta al config.yaml")
    parser.add_argument("--format", choices=["parquet", "csv"], help="Formato de salida (override)")

    args = parser.parse_args()

    # Banner
    logger.info("╔══════════════════════════════════════════════════════════╗")
    logger.info("║  BCIE — Laboratorio de Analítica Avanzada v2.0.0        ║")
    logger.info("║  Arquitectura Medallón | Pipeline de Producción         ║")
    logger.info("╚══════════════════════════════════════════════════════════╝")
    logger.info(f"  Modo: {args.mode} | Modelo: {args.model or 'todos'} | ETL: {'skip' if args.skip_etl else 'ejecutar'}")

    start_time = time.time()

    # Cargar configuración
    config = load_config(args.config)

    if args.format:
        config["paths"]["format"] = args.format

    # --- ETL (Bronze + Silver) ---
    df_clustering = df_forecasting = None

    if args.mode in ["all", "etl"] and not args.skip_etl:
        df_bronze = run_bronze(config)
        df_clustering, df_forecasting = run_silver(df_bronze, config)
    else:
        # Cargar desde Silver existente
        import pandas as pd
        silver_dir = Path(config["paths"]["silver"])
        fmt = config["paths"].get("format", "parquet")

        clust_path = silver_dir / f"aprobaciones_clustering.{fmt}"
        fc_path = silver_dir / f"aprobaciones_forecasting.{fmt}"

        if clust_path.exists():
            df_clustering = pd.read_parquet(clust_path) if fmt == "parquet" else pd.read_csv(clust_path)
            logger.info(f"Silver cargado: clustering ({len(df_clustering):,} registros)")
        if fc_path.exists():
            df_forecasting = pd.read_parquet(fc_path) if fmt == "parquet" else pd.read_csv(fc_path)
            logger.info(f"Silver cargado: forecasting ({len(df_forecasting):,} registros)")

    if args.mode == "etl":
        elapsed = time.time() - start_time
        logger.info(f"ETL completado en {elapsed:.1f}s")
        return

    # --- Clustering (Gold) ---
    clustering_results = {}
    if args.mode in ["all", "clustering"] and df_clustering is not None:
        model_filter = args.model if args.model in [
            "kmeans", "kmedoids", "hdbscan", "dbscan", "hierarchical", "gmm", "mixed"
        ] else None
        clustering_results = run_clustering(df_clustering, config, model_filter)

    # --- Forecasting (Gold) ---
    forecasting_results = {}
    if args.mode in ["all", "forecasting"] and df_forecasting is not None:
        model_filter = args.model if args.model in [
            "prophet", "neuralprophet", "statsforecast", "timesfm"
        ] else None
        forecasting_results = run_forecasting(df_forecasting, config, model_filter)

    # --- Dashboard ---
    if args.mode in ["all", "dashboard"]:
        run_dashboard(config, clustering_results, forecasting_results)

    elapsed = time.time() - start_time
    logger.info(f"━━━ PIPELINE COMPLETADO EN {elapsed:.1f}s ━━━")


if __name__ == "__main__":
    main()
