---
description: Ejecuta un discovery del estado de los modelos ML del laboratorio BCIE
---

# Discovery — BCIE ML Lab

## Pasos del Discovery

### 1. Estado de Modelos

// turbo

- Listar todos los directorios dentro de `models/`
- Para cada modelo, verificar si tiene: `run.py`, `config/`, `src/`, `data/`, `requirements.txt`
- Identificar modelos completos vs incompletos

### 2. Auditoría de Modelos

// turbo

- Leer `models/AUDITORIA_MODELOS.md` (si existe)
- Leer `models/checklist_modelos.csv` (si existe)
- Identificar modelos con issues pendientes

### 3. Estado del Repositorio Git

- Ejecutar `git status` en `D:\BCIE\Datos-Abiertos-BCIE`
- Verificar si hay cambios sin commitear
- Verificar branches activos

### 4. Dashboards Generados

// turbo

- Buscar archivos HTML en `data/05-plots/` de cada modelo
- Verificar que los dashboards más recientes estén actualizados

### 5. Dependencias

// turbo

- Verificar si el `.venv` existe y está activo
- Revisar `app/requirements.txt` para paquetes desactualizados

### 6. Generar Reporte

Generar un reporte con:

- 📊 Modelos activos y su estado
- ✅ Pipelines que corren correctamente
- ⚠️ Modelos con issues o incompletos
- 🔧 Dependencias desactualizadas
- 🎯 Próximos modelos sugeridos
- 📋 Estado del repositorio Git
