---
description: Guía para crear un nuevo modelo ML en el laboratorio BCIE
---

# Crear Nuevo Modelo — BCIE ML Lab

## Pre-requisitos

1. Ejecutar `/load-context` si no se ha cargado el contexto
2. Verificar ambiente con `python verify_env.py`
3. Activar el entorno virtual: `.venv\Scripts\activate` (Windows)

## Flujo de Creación

### Paso 1: Scaffolding del Modelo

1. Editar `setup_project.py` cambiando `PROJECT_NAME` al nombre del nuevo modelo
2. Ejecutar `python setup_project.py`
3. Esto crea la estructura estándar:
   ```
   models/<nombre_modelo>/
   ├── config/local.yaml
   ├── data/01-raw/ a 05-plots/
   ├── src/pipelines/ (etl, training)
   ├── src/dashboard/
   ├── src/utils/
   ├── run.py
   └── requirements.txt
   ```

### Paso 2: Configuración

1. Editar `config/local.yaml`:
   - Definir `api.base_url`, `api.resource_id` para el endpoint CKAN
   - Configurar columnas objetivo y features
   - Definir hiperparámetros del modelo
2. Agregar dependencias específicas a `requirements.txt`

### Paso 3: ETL Pipeline

1. Implementar `src/pipelines/etl_pipeline.py`:
   - Fetch desde CKAN API → `data/01-raw/`
   - Limpieza y transformación → `data/02-preprocessed/`
   - Feature engineering → `data/03-features/`

### Paso 4: Training Pipeline

1. Implementar `src/pipelines/training_pipeline.py`:
   - Cargar datos preprocesados
   - Entrenar modelo con hiperparámetros del YAML
   - Guardar predicciones en `data/04-predictions/runs/run_YYYYMMDD_HHMMSS_<uuid>/`
   - Guardar métricas en JSON

### Paso 5: Dashboard

1. Implementar `src/dashboard/generate_dashboard.py`:
   - Leer predicciones y métricas
   - Generar dashboard HTML standalone con Plotly
   - Guardar en `data/05-plots/`

### Paso 6: Orquestador

1. Verificar que `run.py` orqueste las 3 fases:
   ```bash
   python run.py                    # Pipeline completo
   python run.py --skip-etl         # Sin re-descargar datos
   python run.py --optimize         # Con optimización de hiperparámetros
   ```

### Paso 7: Validación y Registro

1. Ejecutar el pipeline completo y verificar resultados
2. Agregar el modelo al checklist en `models/checklist_modelos.csv`
3. Commit: `feat(models): add <nombre_modelo> pipeline`
4. Push al repositorio

## Convenciones de Código

- Usar type hints en todas las funciones
- Docstrings en formato Google
- Logging con `logging` (no `print`)
- Nunca hardcodear paths — usar `config/local.yaml`
