import pandas as pd
import json

print('='*80)
print('VERIFICACIÓN: Proyección Inicial por Modelo')
print('='*80)

# Check what the per-country data gives as totals for each year
for model in ['neuralprophet', 'prophet', 'statsforecast', 'timesfm']:
    df = pd.read_parquet(f'app/data/gold/forecasting/{model}/predicciones.parquet')
    df['year'] = df['ds'].dt.year
    
    print(f'\n{model.upper()}:')
    print(f'  Años en el parquet: {sorted(df["year"].unique())}')
    print(f'  Países: {sorted(df["Pais"].unique())}')
    
    for yr in sorted(df['year'].unique()):
        sub = df[df['year'] == yr]
        total = sub['yhat'].sum()
        n_countries = len(sub)
        print(f'  {yr}: ${total:>15,.0f}  ({n_countries} países)')

# Read chart trace data
print('\n' + '='*80)
print('DATOS EN LOS GRÁFICOS PLOTLY (lo que muestra el KPI):')
print('='*80)

html = open('app/data/gold/dashboard/dashboard_unificado.html', 'r', encoding='utf-8').read()

# Find CHARTS JSON
import re
charts_start = html.find('const CHARTS = {')
if charts_start >= 0:
    # Extract just the forecast chart keys
    for model in ['neuralprophet', 'prophet', 'statsforecast', 'timesfm']:
        key = f'forecast_{model}'
        key_pos = html.find(f'"{key}"', charts_start)
        if key_pos < 0:
            continue
        # Find the JSON value (between first { and matching })
        json_start = html.find('{', key_pos + len(key) + 5)
        # Count braces to find matching close
        depth = 0
        json_end = json_start
        for i in range(json_start, min(json_start + 50000, len(html))):
            if html[i] == '{':
                depth += 1
            elif html[i] == '}':
                depth -= 1
                if depth == 0:
                    json_end = i + 1
                    break
        
        chart_json = html[json_start:json_end]
        # Unescape the JSON
        chart_json = chart_json.replace('\\"', '"')
        try:
            chart = json.loads(chart_json)
            trace1 = chart['data'][1]  # Pronóstico trace
            print(f'\n{model.upper()} - Trace "Pronóstico":')
            print(f'  Nombre: {trace1.get("name", "N/A")}')
            for x, y in zip(trace1['x'], trace1['y']):
                print(f'  {x}: ${y:>15,.0f}')
            print(f'  KPI Proyección Inicial = ${trace1["y"][0]:>15,.0f}  (primer valor)')
            print(f'  KPI Proyección Final   = ${trace1["y"][-1]:>15,.0f}  (último valor)')
        except Exception as e:
            print(f'  Error parsing: {e}')
