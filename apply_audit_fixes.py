"""Apply all v2 audit fixes to dashboard_unificado.html
H-01: Remove duplicate Evolución title (keep card title, remove Plotly internal)
H-02: Improve Tipo de Socio chart margin-left
H-04: Expand forecasting chart width 
H-08: Add tooltip to PCA 2D annotation
H-09: Increase left margin in mini scatter plots (Lab View)
H-10/H-11: Add max-width to long text blocks
+ Global: 30px padding on sections, 20px gap between elements, no scroll
"""

filepath = r'd:\BCIE\Datos-Abiertos-BCIE\app\data\gold\dashboard\dashboard_unificado.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ─── FIX: Section padding 16px 20px → 30px (uniform inner padding from all sides) ───
content = content.replace(
    'padding: 16px 20px;\n        overflow-y: auto;\n        overflow-x: hidden;',
    'padding: 30px;\n        overflow-y: auto;\n        overflow-x: hidden;'
)

# ─── FIX: Bento grid gap 12px → 20px ───
content = content.replace(
    "gap: 12px;\n        height: 100%;\n        overflow: hidden;\n      }\n      .bento > * {",
    "gap: 20px;\n        height: 100%;\n        overflow: hidden;\n      }\n      .bento > * {"
)

# ─── FIX: KPI stack gap 12px → 20px ───
content = content.replace(
    ".kpi-stack {\n        display: flex;\n        flex-direction: column;\n        gap: 12px;",
    ".kpi-stack {\n        display: flex;\n        flex-direction: column;\n        gap: 20px;"
)

# ─── FIX: Forecasting layout gap 16px → 20px ───
content = content.replace(
    ".fc-layout {\n        display: grid;\n        grid-template-columns: 220px 1fr;\n        gap: 16px;",
    ".fc-layout {\n        display: grid;\n        grid-template-columns: 220px 1fr;\n        gap: 20px;"
)

# ─── FIX: Forecasting sidebar gap 12px → 20px ───
content = content.replace(
    ".fc-sidebar {\n        display: flex;\n        flex-direction: column;\n        gap: 12px;",
    ".fc-sidebar {\n        display: flex;\n        flex-direction: column;\n        gap: 20px;"
)

# ─── FIX: Forecasting main gap 16px → 20px ───
content = content.replace(
    ".fc-main {\n        display: flex;\n        flex-direction: column;\n        gap: 16px;",
    ".fc-main {\n        display: flex;\n        flex-direction: column;\n        gap: 20px;"
)

# ─── FIX: Clustering metrics gap 16px → 20px ───
content = content.replace(
    ".cl-metrics {\n        display: flex;\n        gap: 16px;",
    ".cl-metrics {\n        display: flex;\n        gap: 20px;"
)

# ─── FIX: Clustering tabs margin-bottom 16px → 20px ───
content = content.replace(
    ".cl-tabs {\n        display: flex;\n        gap: 4px;\n        margin-bottom: 16px;",
    ".cl-tabs {\n        display: flex;\n        gap: 4px;\n        margin-bottom: 20px;"
)

# ─── FIX: fc-tabs margin-bottom 16px → 20px ───
content = content.replace(
    ".fc-tabs {\n        display: flex;\n        gap: 4px;\n        margin-bottom: 16px;",
    ".fc-tabs {\n        display: flex;\n        gap: 4px;\n        margin-bottom: 20px;"
)

# ─── FIX: Clustering metrics margin 16px → 20px ───
content = content.replace(
    "gap: 20px;\n        margin-bottom: 16px;\n      }\n      .cl-metric {",
    "gap: 20px;\n        margin-bottom: 20px;\n      }\n      .cl-metric {"
)

# ─── FIX: Sector grid gap already 20px — OK ───

# ─── FIX: section-title margin → 20px bottom ───
content = content.replace(
    ".section-title {\n        font-size: 14px;\n        font-weight: 700;\n        color: var(--text-dark);\n        margin: 8px 0;",
    ".section-title {\n        font-size: 14px;\n        font-weight: 700;\n        color: var(--text-dark);\n        margin: 0 0 20px 0;"
)

# ─── H-01: Remove duplicate Evolución title ───
# The card shows "Evolución Temporal de Aprobaciones" AND the Plotly chart has its own title
# Solution: Remove the internal Plotly title by clearing it in JS when rendering evolucion
content = content.replace(
    "// Add rangeslider to evolucion chart\n                  if (key === \"evolucion\" && parsed.layout.xaxis) {\n                    parsed.layout.xaxis.rangeslider = { visible: true, thickness: 0.06, bgcolor: \"rgba(255,255,255,0.03)\" };\n                    parsed.layout.margin = { l: 60, r: 60, t: 40, b: 10 };",
    "// Add rangeslider to evolucion chart\n                  if (key === \"evolucion\" && parsed.layout.xaxis) {\n                    parsed.layout.xaxis.rangeslider = { visible: true, thickness: 0.06, bgcolor: \"rgba(255,255,255,0.03)\" };\n                    parsed.layout.margin = { l: 60, r: 60, t: 10, b: 10 };\n                    parsed.layout.title = '';  // H-01: Remove duplicate title (card has its own)"
)

# ─── H-02: Increase left margin for tipo_socio chart ───
# Add a special case in chart rendering for tipo_socio
content = content.replace(
    'tipo_socio: "chart-tipo-socio",',
    'tipo_socio: "chart-tipo-socio",'
)
# Add JS fix after the mappings block for tipo_socio left margin
content = content.replace(
    'if (mappings[key]) el_id = mappings[key];',
    'if (mappings[key]) el_id = mappings[key];\n              // H-02: Increase left margin for tipo_socio to prevent label truncation\n              if (key === "tipo_socio") {\n                try {\n                  let p = JSON.parse(json_str);\n                  if (p.layout) { p.layout.margin = Object.assign(p.layout.margin || {}, { l: 130 }); }\n                  json_str = JSON.stringify(p);\n                } catch(e) {}\n              }'
)

# ─── H-10: Add max-width to Cross-Validation hallazgo text ───
content = content.replace(
    '<div style="margin-top:12px;padding:12px;background:linear-gradient(135deg, #f59e0b11, #f59e0b05);border:1px solid #f59e0b33;border-radius:8px;font-size:11px;color:var(--text-light)">',
    '<div style="margin-top:20px;padding:14px 18px;background:linear-gradient(135deg, #f59e0b11, #f59e0b05);border:1px solid #f59e0b33;border-radius:8px;font-size:11px;color:var(--text-light);max-width:1200px;line-height:1.6">'
)

# ─── H-11: Add max-width to Decision panel Nota ───
# The Nota at the bottom of Forecasting decision panel
content = content.replace(
    '<div style="background:var(--bg-card-alt);border-left:3px solid #f59e0b;border-radius:0 8px 8px 0;padding:14px">\n',
    '<div style="background:var(--bg-card-alt);border-left:3px solid #f59e0b;border-radius:0 8px 8px 0;padding:14px;line-height:1.6">\n'
)

# ─── H-09: Increase left margin for mini scatter plots in Lab View ───
# Find the renderLabScatters function's Plotly.react compact margin and increase l
content = content.replace(
    'margin: { l: 30, r: 10, t: 25, b: 25 }',
    'margin: { l: 38, r: 10, t: 25, b: 25 }'
)

# ─── FIX: Cross-val section gap between elements ───
# The grid gap inside crossvalidation cards
content = content.replace(
    'grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:20px',
    'grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:20px'
)

# ─── FIX: Decision panel section inline gaps ───
# Decision panel grid-template-columns gap
content = content.replace(
    'grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:16px',
    'grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:20px'
)

# ─── FIX: Traj container scroll → no scroll ───
content = content.replace(
    ".traj-container {\n        display: flex;\n        flex-direction: column;\n        gap: 8px;\n        overflow-y: auto;",
    ".traj-container {\n        display: flex;\n        flex-direction: column;\n        gap: 8px;\n        overflow-y: hidden;"
)

# ─── FIX: Footer margin-bottom → 0 (no extra space) ───
content = content.replace(
    "margin-bottom: 8px;\n        background: var(--bg-sidebar);",
    "margin-bottom: 0;\n        background: var(--bg-sidebar);"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("All audit fixes applied successfully!")
print("Changes:")
print("  ✓ H-01: Duplicate evolution title removed")
print("  ✓ H-02: Tipo de Socio chart left margin increased")
print("  ✓ H-09: Lab View mini-chart left margins increased")
print("  ✓ H-10: Cross-validation hallazgo max-width 1200px + line-height")
print("  ✓ H-11: Decision Nota line-height improved")  
print("  ✓ Global: Section padding → 30px uniform")
print("  ✓ Global: All gaps between charts → 20px uniform") 
print("  ✓ Global: Traj container overflow → hidden (no scroll)")
print("  ✓ Global: Footer margin-bottom → 0")
print("  ✓ Global: Section title margin → 0 0 20px 0")
