import pandas as pd
import json

print('='*80)
print('AUDITORÍA COMPLETA DE DATOS HISTÓRICOS vs PRONÓSTICOS')
print('='*80)

# 1. Historical data from silver layer (ground truth)
hist = pd.read_parquet('app/data/silver/aprobaciones_forecasting.parquet')
hist['year'] = hist['ds'].dt.year

print('\n1. DATOS HISTÓRICOS REALES (Silver Layer)')
print('-'*80)
for y in [2022, 2023, 2024, 2025]:
    sub = hist[hist['year'] == y]
    total = sub['y'].sum()
    print(f'\n  AÑO {y} - Total: ${total:,.0f}')
    for _, row in sub.sort_values('Pais').iterrows():
        pais = row['Pais']
        val = row['y']
        print(f'    {pais:30s} ${val:>15,.0f}')

# 2. Check what years each model predicts
print('\n\n2. PRONÓSTICOS POR MODELO')
print('-'*80)
for model in ['neuralprophet', 'prophet', 'statsforecast', 'timesfm']:
    df = pd.read_parquet(f'app/data/gold/forecasting/{model}/predicciones.parquet')
    df['year'] = df['ds'].dt.year
    years = sorted(df['year'].unique())
    countries = sorted(df['Pais'].unique())
    print(f'\n  {model.upper()}:')
    print(f'    Años predichos: {years}')
    print(f'    Países: {len(countries)}')
    
    hist_overlap = df[df['year'].isin([2024, 2025])]
    if len(hist_overlap) > 0:
        print(f'    *** OVERLAP CON AÑOS HISTÓRICOS:')
        for _, row in hist_overlap.sort_values(['year', 'Pais']).iterrows():
            pais = row['Pais']
            yr = row['year']
            yhat = row['yhat']
            real = hist[(hist['Pais'] == pais) & (hist['year'] == yr)]
            if len(real) > 0:
                rv = real.iloc[0]['y']
                diff = yhat - rv
                print(f'       {pais:25s} {yr} fc=${yhat:>13,.0f}  real=${rv:>13,.0f}  diff={diff:+,.0f}')
            else:
                print(f'       {pais:25s} {yr} fc=${yhat:>13,.0f}  real=N/A')

# 3. Show what table currently displays for 2024-2025
print('\n\n3. PROBLEMA EN JS: modelData se revisa ANTES que histData')
print('-'*80)
print('  Para Belice, Prophet/StatsF/TimesFM tienen forecasts para 2024-2025')
print('  que sobreescriben los datos historicos reales.')
print('  Solucion: Para 2024-2025, siempre priorizar datos historicos.')

# 4. Also verify NeuralProphet has NO 2024-2025 data
print('\n\n4. NeuralProphet: solo predice 2026-2030')
df_np = pd.read_parquet('app/data/gold/forecasting/neuralprophet/predicciones.parquet')
print(f'  Años: {sorted(df_np["ds"].dt.year.unique())}')
print(f'  Paises: {sorted(df_np["Pais"].unique())}')
print(f'  NO incluye Belice, Cuba, Mexico, Regional (paises sin suficiente historial)')
