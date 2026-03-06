# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Machine Learning laboratory for reproducible experiments using open data from BCIE (Banco Centroamericano de Integración Económica). The repository contains multiple independent ML models focused on approvals forecasting and clustering analysis.

**Data Source:** BCIE Open Data Portal (CKAN API) - https://datosabiertos.bcie.org/

## Commands

### Running a Model Pipeline

Each model in `models/` is self-contained. Navigate to the model directory and run:

```bash
cd models/<model_name>
python run.py                           # Full pipeline: ETL → Training → Dashboard
python run.py --skip-etl                # Skip data extraction if already cached
python run.py --optimize                # Run with hyperparameter optimization
python run.py --config config/local.yaml  # Specify config file
```

### Environment Verification

```bash
python verify_env.py   # Check all required ML libraries are installed
```

### Creating a New Model Project

Edit `setup_project.py` to change `PROJECT_NAME`, then run:

```bash
python setup_project.py
```

### Installing Dependencies

Each model has its own requirements.txt:

```bash
cd models/<model_name>
pip install -r requirements.txt
```

## Architecture

### Model Directory Structure

Every model follows a standardized 3-phase pipeline pattern:

```
models/<model_name>/
├── config/local.yaml       # API endpoints, hyperparameters, paths
├── data/
│   ├── 01-raw/            # Raw data from CKAN API
│   ├── 02-preprocessed/   # Cleaned/transformed data
│   ├── 03-features/       # Feature engineering output
│   ├── 04-predictions/    # Model outputs (runs/ for versioned results)
│   └── 05-plots/          # Generated HTML dashboards
├── src/
│   ├── pipelines/         # ETL, training, optimization orchestration
│   ├── dashboard/         # Plotly HTML generation
│   └── utils/             # Helpers (Gower distance, embeddings, etc.)
├── run.py                 # Main orchestrator
└── requirements.txt
```

### Pipeline Phases

1. **ETL** (`src/pipelines/etl_pipeline.py`): Fetch from CKAN API → Clean → Save to `data/02-preprocessed/`
2. **Training** (`src/pipelines/training_pipeline.py`): Load data → Fit model → Save predictions to `data/04-predictions/`
3. **Dashboard** (`src/dashboard/generate_dashboard.py`): Generate interactive HTML visualizations

### Configuration

Models use YAML configuration (`config/local.yaml`) for:
- API settings (base_url, resource_id, limit)
- Data paths and column mappings
- Model hyperparameters
- Output directories

### Model Types Implemented

- **Time Series:** Prophet, NeuralProphet, StatsForecast (AutoARIMA/Theta), TimesFM
- **Clustering:** K-Means, HDBSCAN, Hierarchical, DBSCAN, GMM, K-Medoids
- **Mixed Data Clustering:** Gower Distance for categorical + numeric features

### Key Libraries

pandas, numpy, scikit-learn, prophet, neuralprophet, statsforecast, hdbscan, xgboost, plotly, torch, transformers

## Unified Dashboard

The main dashboard is at `app/data/gold/dashboard/dashboard_unificado.html`. It is a single-page standalone HTML application using Plotly.js with sidebar navigation.

### Sections

- **Inicio** (sec-home): Landing page with KPIs, evolution charts, and annual summary table
- **Forecasting** (sec-forecasting): Tabs for Prophet, NeuralProphet, StatsForecast, TimesFM models with projection charts and forecast matrices
- **Clustering** (sec-clustering): Two view modes:
  - **Individual**: Tabbed panels per model (DBSCAN, GMM, HDBSCAN, Hierarchical, KMeans, KMedoids, Mixed) with full scatter plot and cluster profiles
  - **Lab View**: All 7 models side-by-side in a 4-column CSS grid + summary card
- **Administration** (sec-admin): Admin panel link

### Key Functions (JavaScript)

- `applyPCA2D(parsed)`: Transforms raw scatter data into PCA-like 2D projection with log scaling, rotation, and jitter. Sets axis ranges with padding and enforces Y-axis minimum of -2.
- `renderLabScatters()`: Renders mini scatter plots in Lab View with compact margins and marker size 5. Called lazily on first Lab View toggle.
- `showClModel(name)`: Switches between individual clustering model tabs.
- `toggleClView(mode)`: Toggles between Individual and Lab View.

### Chart Data Pipeline

Chart data is embedded in a `CHARTS` object as JSON strings, keyed by chart identifier (e.g., `scatter_dbscan`, `evolucion`, `forecast_prophet`). The `sync_forecasts.py` script ensures data consistency between model labs and the unified dashboard.

## Development Notes

- Run IDs are auto-generated with format `run_YYYYMMDD_HHMMSS_<uuid6>` for versioning outputs
- Validation uses Bootstrap ARI, Silhouette scores, and Composite Score optimization
- Dashboards are standalone HTML files with interactive Plotly charts
- Models track status in `models/checklist_modelos.csv`
- Clustering Lab View grid uses `gap: 20px` between chart cards; mini scatter containers are 220px tall
- PCA 2D axis ranges enforce a Y-minimum of -2 to prevent bottom data points from being clipped
- **Icons: SVG only.** All icons in the unified dashboard MUST be inline SVGs (no emoji characters). Use `<svg viewBox="0 0 24 24" ...>` with `display:inline-block;vertical-align:middle` for text-flow alignment. Never use emoji (📊, ⭐, ✅, etc.) — always convert to corresponding SVG icons.
