import json, re

html = open(r'D:\BCIE\Datos-Abiertos-BCIE\app\data\gold\dashboard\dashboard_unificado.html', 'r', encoding='utf-8').read()

# Find FC_COUNTRY_DATA
fc_start = html.find('const FC_COUNTRY_DATA = {')
if fc_start >= 0:
    depth = 0
    fc_end = fc_start
    for i in range(fc_start + 24, min(fc_start + 100000, len(html))):
        if html[i] == '{': depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                fc_end = i + 1
                break
    fc_json_str = html[fc_start + 24:fc_end]
    fc_data = json.loads(fc_json_str)
    
    print("NeuralProphet year totals from FC_COUNTRY_DATA:")
    np_data = fc_data['fc']['neuralprophet']
    for yr in ['2026','2027','2028','2029','2030']:
        total = sum(np_data[c].get(yr, 0) for c in np_data)
        print(f"  {yr}: ${total:,.0f}")

# Now check what the Plotly trace has
charts_start = html.find('const CHARTS = {')
np_key_pos = html.find('"forecast_neuralprophet"', charts_start)
if np_key_pos > 0:
    colon_pos = html.index(':', np_key_pos + 25)
    q1 = html.index('"', colon_pos + 1)
    i = q1 + 1
    while i < len(html):
        if html[i] == '\\':
            i += 2
            continue
        if html[i] == '"':
            break
        i += 1
    raw_json = html[q1+1:i]
    raw_json = raw_json.replace('\\"', '"').replace('\\\\', '\\')
    chart = json.loads(raw_json)
    
    print("\nPlotly CHART trace data for NeuralProphet:")
    for t_idx, trace in enumerate(chart['data']):
        print(f"  Trace {t_idx}: {trace.get('name', 'N/A')}")
        if 'x' in trace and 'y' in trace:
            for x, y in zip(trace['x'], trace['y']):
                yr = x[:4] if isinstance(x, str) else str(x)
                val = f"${y:,.0f}" if isinstance(y, (int, float)) else str(y)
                print(f"    {yr}: {val}")
    
    print(f"\nLayout title: {chart['layout'].get('title', 'N/A')}")
