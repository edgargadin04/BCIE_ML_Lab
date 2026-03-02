---
description: Carga el contexto del laboratorio de ML con datos abiertos del BCIE
---

# Contexto del Proyecto: Laboratorio ML — Datos Abiertos BCIE

## Identidad del Proyecto

- **Nombre:** Laboratorio de Machine Learning: Datos Abiertos del BCIE
- **Repositorio:** `D:\BCIE\Datos-Abiertos-BCIE` (GitHub: NORSAB/Datos-Abiertos-BCIE)
- **Objetivo:** Transformar datos públicos del BCIE en inteligencia predictiva y segmentación estratégica
- **Fuente de datos:** Portal BCIE (CKAN API) — https://datosabiertos.bcie.org/
- **Autor principal:** Norman Reynaldo Sabillon Castro

## Arquitectura del Pipeline

Cada modelo sigue 3 fases:

1. **ETL** → `src/pipelines/etl_pipeline.py` (CKAN API → limpieza → `data/02-preprocessed/`)
2. **Training** → `src/pipelines/training_pipeline.py` (modelo → predicciones → `data/04-predictions/`)
3. **Dashboard** → `src/dashboard/generate_dashboard.py` (HTML interactivo con Plotly)

## Modelos Implementados (12 activos)

### Clustering (Segmentación de Cartera)

| Modelo           | Resultado                                  |
| ---------------- | ------------------------------------------ |
| DBSCAN           | 3 Tiers + Ruido (eps=0.25, min_samples=10) |
| K-Means          | K=4 Clusters                               |
| Hierarchical     | K=4 Clusters (Ward)                        |
| Mixed (Ensemble) | K=3 Clusters (Score 0.85)                  |
| HDBSCAN          | 14 Micro-clusters                          |

### Forecasting (Proyección de Aprobaciones)

| Modelo        | Enfoque                             |
| ------------- | ----------------------------------- |
| TimesFM       | Foundation Model Zero-Shot (Google) |
| StatsForecast | AutoARIMA + Theta (Nixtla)          |
| Prophet       | Modelo Aditivo (Meta)               |
| NeuralProphet | Híbrido AR-Net                      |

## Stack Tecnológico

pandas, numpy, scikit-learn, prophet, neuralprophet, statsforecast, hdbscan, xgboost, plotly, torch, transformers

## Archivos Clave

- **Configuración:** `app/config.yaml`
- **Punto de entrada:** `app/main.py`
- **Requirements:** `app/requirements.txt`
- **Documentación existente:** `CLAUDE.md`, `README.md`
- **Auditoría:** `models/AUDITORIA_MODELOS.md`

## Convenciones

- Run IDs: `run_YYYYMMDD_HHMMSS_<uuid6>`
- Métricas: Bootstrap ARI, Silhouette, Composite Score
- Dashboards: HTML standalone con Plotly interactivo

## Instrucciones para el Agente

1. Al recibir `/load-context`, lee este archivo y responde: "✅ Contexto de BCIE ML Lab cargado"
2. Nuevos modelos deben crearse con `setup_project.py` (editar `PROJECT_NAME` primero)
3. Respetar la estructura de carpetas: `config/`, `src/pipelines/`, `src/dashboard/`, `data/01-raw/` a `data/05-plots/`
4. Todo modelo debe generar un dashboard HTML auto-contenido
5. Verificar ambiente con `verify_env.py` antes de ejecutar pipelines
6. Los datos crudos NUNCA se modifican — toda transformación va en `02-preprocessed/` en adelante
