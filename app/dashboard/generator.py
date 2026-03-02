"""
BCIE — Generador de Dashboard Ejecutivo Premium.

Replica el estilo del Dashboard Ejecutivo de Prophet:
- Layout Bento-box con KPIs prominentes
- Tabla de Detalle Anual con variaciones YoY
- Gráficos de dona por sector institucional
- Distribución por país y tipo de socio
- Forecasting estilo estratégico con filtros laterales

Produce un archivo HTML autocontenido interactivo.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from core.logger import get_logger

logger = get_logger(__name__)


def generate_unified_dashboard(
    config: Dict[str, Any],
    clustering_results: Optional[Dict] = None,
    forecasting_results: Optional[Dict] = None,
) -> Path:
    gold_dir = Path(config["paths"]["gold"])
    fmt = config["paths"].get("format", "parquet")
    output_dir = Path(config["paths"]["dashboard"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Cargar datos
    bronze_df = _load_layer("bronze", config)
    silver_clean = _load_file(Path(config["paths"]["silver"]) / f"aprobaciones_limpias.{fmt}", fmt)
    silver_clust = _load_file(Path(config["paths"]["silver"]) / f"aprobaciones_clustering.{fmt}", fmt)
    silver_fc = _load_file(Path(config["paths"]["silver"]) / f"aprobaciones_forecasting.{fmt}", fmt)
    clustering_data = _load_clustering_data(gold_dir, fmt)
    forecasting_data = _load_forecasting_data(gold_dir, fmt)
    comparison = _load_file(gold_dir / f"comparativa_clustering.{fmt}", fmt)

    # Preparar todos los datos para el HTML
    import plotly.graph_objects as go
    import plotly.io as pio

    charts = {}
    data_payload = {}

    # ── KPIs ──
    if silver_clean is not None:
        total_monto = silver_clean["Monto_Aprobado"].sum() if "Monto_Aprobado" in silver_clean.columns else 0
        qty_col = "CANTIDAD_APROBACIONES" if "CANTIDAD_APROBACIONES" in silver_clean.columns else "Cantidad_Aprobaciones"
        total_aprobaciones = int(silver_clean[qty_col].sum()) if qty_col in silver_clean.columns else 0
        n_paises = silver_clean["Pais"].nunique() if "Pais" in silver_clean.columns else 0
    else:
        total_monto = 0
        total_aprobaciones = len(bronze_df) if bronze_df is not None else 0
        n_paises = 0
    n_modelos = len(clustering_data) + len(forecasting_data)

    # ── Detalle Anual (para tabla YoY) ──
    annual_data = []
    if silver_fc is not None and "ds" in silver_fc.columns and "y" in silver_fc.columns:
        sf = silver_fc.copy()
        sf["ds"] = pd.to_datetime(sf["ds"])
        sf["year"] = sf["ds"].dt.year
        yearly = sf.groupby("year").agg(monto=("y", "sum"), cant=("y", "count")).reset_index()
        yearly = yearly.sort_values("year", ascending=False)
        yearly["promedio"] = yearly["monto"] / yearly["cant"].replace(0, 1)
        yearly["var_monto"] = yearly["monto"].pct_change(periods=-1) * 100
        yearly["var_cant"] = yearly["cant"].pct_change(periods=-1) * 100
        for _, r in yearly.iterrows():
            annual_data.append({
                "year": int(r["year"]),
                "monto": float(r["monto"]),
                "cant": int(r["cant"]),
                "promedio": float(r["promedio"]),
                "var_monto": float(r["var_monto"]) if pd.notna(r["var_monto"]) else None,
                "var_cant": float(r["var_cant"]) if pd.notna(r["var_cant"]) else None,
            })
    data_payload["annual"] = annual_data

    # ── Evolución Temporal (gráfico principal) ──
    if silver_fc is not None and "ds" in silver_fc.columns:
        trend = silver_fc.groupby("ds")["y"].sum().reset_index()
        trend["ds"] = pd.to_datetime(trend["ds"])
        trend = trend.sort_values("ds")
        cnt_trend = silver_fc.groupby("ds")["y"].count().reset_index()
        cnt_trend.columns = ["ds", "cnt"]
        cnt_trend["ds"] = pd.to_datetime(cnt_trend["ds"])
        trend = trend.merge(cnt_trend, on="ds", how="left")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend["ds"], y=trend["y"], mode="lines+markers",
            name="Monto Total Aprobado",
            line=dict(color="#06b6d4", width=2.5),
            marker=dict(size=4, color="#06b6d4"),
            yaxis="y",
            hovertemplate="<b>%{x|%Y}</b><br>$%{y:,.0f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=trend["ds"], y=trend["cnt"], mode="lines+markers",
            name="Cantidad de Aprobaciones",
            line=dict(color="#94a3b8", width=1.5, dash="dot"),
            marker=dict(size=3, color="#94a3b8"),
            yaxis="y2",
            hovertemplate="<b>%{x|%Y}</b><br>%{y} aprobaciones<extra></extra>",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#94a3b8", size=11),
            title=dict(text="Evolución Temporal de Aprobaciones", font=dict(size=14, color="#e2e8f0")),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Monto (USD)", gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)", side="left"),
            yaxis2=dict(title="Cantidad", overlaying="y", side="right", showgrid=False),
            legend=dict(font=dict(color="#e2e8f0", size=10), orientation="h", y=-0.15, x=0.5, xanchor="center"),
            margin=dict(l=60, r=60, t=40, b=50), height=350,
            hovermode="x unified",
        )
        charts["evolucion"] = pio.to_json(fig)

    # ── Distribución Sector (donuts) ──
    if silver_clust is not None and "Sector" in silver_clust.columns:
        sec_monto = silver_clust.groupby("Sector")["Monto_Aprobado"].sum().reset_index()
        sec_cant = silver_clust.groupby("Sector")["Monto_Aprobado"].count().reset_index()
        sec_cant.columns = ["Sector", "Cantidad"]
        donut_colors = ["#105682", "#06b6d4", "#22c55e", "#f59e0b"]

        fig_m = go.Figure(go.Pie(labels=sec_monto["Sector"], values=sec_monto["Monto_Aprobado"], hole=0.6,
                                  marker=dict(colors=donut_colors[:len(sec_monto)]),
                                  textinfo="percent", textfont=dict(size=13, color="white"),
                                  hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>"))
        fig_m.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Inter", color="#94a3b8"), showlegend=False,
                            margin=dict(l=10, r=10, t=10, b=10), height=220,
                            annotations=[dict(text="Monto", x=0.5, y=0.5, font_size=13, font_color="#e2e8f0", showarrow=False)])
        charts["donut_monto"] = pio.to_json(fig_m)

        fig_c = go.Figure(go.Pie(labels=sec_cant["Sector"], values=sec_cant["Cantidad"], hole=0.6,
                                  marker=dict(colors=donut_colors[:len(sec_cant)]),
                                  textinfo="percent", textfont=dict(size=13, color="white"),
                                  hovertemplate="<b>%{label}</b><br>%{value} aprobaciones<br>%{percent}<extra></extra>"))
        fig_c.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Inter", color="#94a3b8"), showlegend=False,
                            margin=dict(l=10, r=10, t=10, b=10), height=220,
                            annotations=[dict(text="Cantidad", x=0.5, y=0.5, font_size=13, font_color="#e2e8f0", showarrow=False)])
        charts["donut_cant"] = pio.to_json(fig_c)

        # Sector detail for legend
        data_payload["sector"] = []
        for _, r in sec_monto.iterrows():
            q = sec_cant[sec_cant["Sector"] == r["Sector"]]["Cantidad"].values
            data_payload["sector"].append({
                "name": r["Sector"],
                "monto": float(r["Monto_Aprobado"]),
                "cantidad": int(q[0]) if len(q) > 0 else 0,
                "promedio": float(r["Monto_Aprobado"] / (q[0] if len(q) > 0 and q[0] > 0 else 1)),
            })

    # ── Tipo de Socio (barras horizontales) ──
    if silver_clust is not None and "Tipo_Pais" in silver_clust.columns:
        tipo = silver_clust.groupby("Tipo_Pais")["Monto_Aprobado"].sum().sort_values().reset_index()
        fig_tipo = go.Figure(go.Bar(
            y=tipo["Tipo_Pais"], x=tipo["Monto_Aprobado"], orientation="h",
            marker=dict(color="#105682"),
            text=[f"USD {v:,.0f}" for v in tipo["Monto_Aprobado"]],
            textposition="outside", textfont=dict(size=10, color="#94a3b8"),
            hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
        ))
        fig_tipo.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=11),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(automargin=True, gridcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=120, t=10, b=10), height=200,
        )
        charts["tipo_socio"] = pio.to_json(fig_tipo)

    # ── Participación por País (barras verticales) ──
    if silver_clust is not None and "Pais" in silver_clust.columns:
        pais = silver_clust.groupby("Pais")["Monto_Aprobado"].sum().sort_values(ascending=False).reset_index()
        fig_pais = go.Figure(go.Bar(
            x=pais["Pais"], y=pais["Monto_Aprobado"],
            marker=dict(color="#22c55e"),
            text=[f"USD {v:,.0f}" for v in pais["Monto_Aprobado"]],
            textposition="outside", textfont=dict(size=8, color="#94a3b8"),
            hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
        ))
        fig_pais.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=10),
            xaxis=dict(tickangle=-45, gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(showgrid=False, showticklabels=False),
            margin=dict(l=10, r=10, t=10, b=80), height=300,
        )
        charts["pais_bars"] = pio.to_json(fig_pais)

    # ── FORECASTING: gráficos por modelo con histórico + proyección ──
    for name, result in forecasting_data.items():
        df = result.get("data")
        if df is None or len(df) == 0:
            continue
        df["ds"] = pd.to_datetime(df["ds"])

        # Gráfico de proyección consolidado (todos los países, línea agregada)
        total_fc = df.groupby("ds").agg(
            yhat=("yhat", "sum"),
            yhat_lower=("yhat_lower", "sum") if "yhat_lower" in df.columns else ("yhat", "sum"),
            yhat_upper=("yhat_upper", "sum") if "yhat_upper" in df.columns else ("yhat", "sum"),
        ).reset_index()

        # Crear histórico + forecast combinado
        fig_fc = go.Figure()

        # Agregar datos históricos si existen
        if silver_fc is not None:
            hist = silver_fc.groupby("ds")["y"].sum().reset_index()
            hist["ds"] = pd.to_datetime(hist["ds"])
            hist = hist.sort_values("ds")
            fig_fc.add_trace(go.Scatter(
                x=hist["ds"], y=hist["y"], mode="lines+markers", name="Histórico",
                line=dict(color="#e2e8f0", width=2), marker=dict(size=3, color="#e2e8f0"),
                hovertemplate="<b>%{x|%Y}</b><br>$%{y:,.0f}<extra>Histórico</extra>",
            ))

        # Forecast
        fig_fc.add_trace(go.Scatter(
            x=total_fc["ds"], y=total_fc["yhat"], mode="lines+markers", name="Pronóstico",
            line=dict(color="#ef4444", width=2.5, dash="dot"), marker=dict(size=5, color="#ef4444"),
            hovertemplate="<b>%{x|%Y}</b><br>$%{y:,.0f}<extra>Pronóstico</extra>",
        ))

        # Banda de confianza
        if "yhat_lower" in total_fc.columns and "yhat_upper" in total_fc.columns:
            fig_fc.add_trace(go.Scatter(
                x=pd.concat([total_fc["ds"], total_fc["ds"][::-1]]),
                y=pd.concat([total_fc["yhat_upper"], total_fc["yhat_lower"][::-1]]),
                fill="toself", fillcolor="rgba(239,68,68,0.15)",
                line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip",
            ))

        fig_fc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8", size=11),
            title=dict(text=f"Tendencia Histórica y Proyección — {name.upper()}", font=dict(size=14, color="#e2e8f0")),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="USD", gridcolor="rgba(255,255,255,0.05)"),
            legend=dict(font=dict(color="#e2e8f0"), orientation="h", y=-0.15, x=0.5, xanchor="center"),
            margin=dict(l=70, r=30, t=50, b=60), height=400,
            hovermode="x unified",
        )
        charts[f"forecast_{name}"] = pio.to_json(fig_fc)

        # Tabla de predicciones por país y año
        fc_table = []
        for pais in sorted(df["Pais"].unique()):
            pdf = df[df["Pais"] == pais].sort_values("ds")
            row = {"Pais": pais}
            for _, r in pdf.iterrows():
                yr = r["ds"].year
                row[str(yr)] = float(r["yhat"])
            fc_table.append(row)
        data_payload[f"fc_matrix_{name}"] = fc_table

        # Trayectoria anual agregada
        traj = []
        total_fc_sorted = total_fc.sort_values("ds")
        for i, (_, r) in enumerate(total_fc_sorted.iterrows()):
            yr = r["ds"].year
            val = float(r["yhat"])
            prev = float(total_fc_sorted.iloc[i-1]["yhat"]) if i > 0 else None
            growth = ((val - prev) / prev * 100) if prev and prev > 0 else None
            traj.append({"year": yr, "value": val, "growth": growth})
        data_payload[f"fc_traj_{name}"] = traj

    # ── CLUSTERING (simplificado) ──
    for name, result in clustering_data.items():
        df = result.get("data")
        if df is None or "Cluster" not in df.columns:
            continue

        xcol = "Monto_Aprobado" if "Monto_Aprobado" in df.columns else df.columns[1]
        ycol = "Cantidad_Aprobaciones" if "Cantidad_Aprobaciones" in df.columns else df.columns[2]
        cluster_colors = ["#6366f1", "#06b6d4", "#22c55e", "#f59e0b", "#ef4444", "#ec4899", "#8b5cf6", "#14b8a6"]

        if xcol in df.columns and ycol in df.columns:
            fig_sc = go.Figure()
            for i, c in enumerate(sorted(df["Cluster"].unique())):
                mask = df["Cluster"] == c
                fig_sc.add_trace(go.Scatter(
                    x=df.loc[mask, xcol] / 1e6 if df[xcol].max() > 1e5 else df.loc[mask, xcol],
                    y=df.loc[mask, ycol], mode="markers",
                    marker=dict(size=9, color=cluster_colors[i % len(cluster_colors)], line=dict(width=1, color="rgba(255,255,255,0.3)")),
                    name=f"Cluster {c}",
                    text=df.loc[mask, "Pais"].values if "Pais" in df.columns else None,
                    hovertemplate="<b>%{text}</b><br>$%{x:,.1f}M<extra></extra>" if "Pais" in df.columns else None,
                ))
            fig_sc.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8", size=11),
                xaxis=dict(title="Monto (USD M)", gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(title="Cantidad", gridcolor="rgba(255,255,255,0.05)"),
                legend=dict(font=dict(color="#e2e8f0"), orientation="h", y=1.08),
                margin=dict(l=50, r=20, t=20, b=40), height=380,
            )
            charts[f"scatter_{name}"] = pio.to_json(fig_sc)

    # ── COMPARATIVA: Radar ──
    if comparison is not None and len(comparison) > 0:
        radar_models = comparison.head(7)
        categories = ["Silhouette", "1/DBI", "CH (norm)", "Estabilidad"]
        fig_radar = go.Figure()
        radar_colors = ["#6366f1", "#06b6d4", "#22c55e", "#f59e0b", "#ef4444", "#ec4899", "#8b5cf6"]
        for i, (_, row) in enumerate(radar_models.iterrows()):
            sil = row.get("silhouette", 0) or 0
            dbi = row.get("davies_bouldin", 1) or 1
            chi = row.get("calinski_harabasz", 0) or 0
            ari = row.get("stability_ari", 0) or 0
            chi_max = comparison["calinski_harabasz"].max() if comparison["calinski_harabasz"].max() > 0 else 1
            vals = [sil, min(1 / max(dbi, 0.01), 5) / 5, chi / chi_max, ari]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=categories + [categories[0]],
                fill="toself", fillcolor=f"rgba({int(radar_colors[i][1:3],16)},{int(radar_colors[i][3:5],16)},{int(radar_colors[i][5:7],16)},0.1)",
                line=dict(color=radar_colors[i], width=2),
                name=row["modelo"].upper(),
            ))
        fig_radar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8"), height=420,
            polar=dict(bgcolor="rgba(0,0,0,0)",
                       radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.1)"),
                       angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")),
            legend=dict(font=dict(color="#e2e8f0", size=10)),
            margin=dict(l=60, r=60, t=30, b=30),
        )
        charts["radar"] = pio.to_json(fig_radar)

    # ── Build HTML ──
    html = _build_executive_html(
        charts, data_payload, clustering_data, forecasting_data, comparison,
        total_aprobaciones, total_monto, n_paises, n_modelos,
        bronze_df, silver_clust, silver_fc, config)

    output_path = output_dir / "dashboard_unificado.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info(f"Dashboard ejecutivo generado: {output_path}")
    logger.info(f"  Gráficos: {len(charts)} | Modelos: {len(clustering_data)} clustering + {len(forecasting_data)} forecasting")
    return output_path


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _load_file(path, fmt):
    p = Path(path)
    if not p.exists():
        return None
    return pd.read_parquet(p) if fmt == "parquet" else pd.read_csv(p)


def _load_layer(name, config):
    p = Path(config["paths"][name])
    for ext in ["parquet", "csv"]:
        f = p / f"aprobaciones_raw.{ext}"
        if f.exists():
            return pd.read_parquet(f) if ext == "parquet" else pd.read_csv(f)
    return None


def _load_clustering_data(gold_dir, fmt):
    results = {}
    clust_dir = gold_dir / "clustering"
    if not clust_dir.exists():
        return results
    for model_dir in sorted(clust_dir.iterdir()):
        if model_dir.is_dir():
            pred = model_dir / f"resultados.{fmt}"
            if not pred.exists():
                pred = model_dir / f"predicciones.{fmt}"
            metrics = model_dir / "metricas.json"
            data = _load_file(pred, fmt)
            m = json.loads(metrics.read_text()) if metrics.exists() else {}
            if data is not None:
                results[model_dir.name] = {"data": data, "metrics": m}
    return results


def _load_forecasting_data(gold_dir, fmt):
    results = {}
    fc_dir = gold_dir / "forecasting"
    if not fc_dir.exists():
        return results
    for model_dir in sorted(fc_dir.iterdir()):
        if model_dir.is_dir():
            pred = model_dir / f"predicciones.{fmt}"
            data = _load_file(pred, fmt)
            if data is not None:
                results[model_dir.name] = {"data": data}
    return results


def _fmt_usd(val):
    """Formato USD ejecutivo."""
    if abs(val) >= 1e9:
        return f"${val/1e9:,.1f}B"
    if abs(val) >= 1e6:
        return f"${val/1e6:,.0f}M"
    return f"${val:,.0f}"


def _build_executive_html(charts, data_payload, clustering_data, forecasting_data,
                          comparison, total_aprobaciones, total_monto, n_paises, n_modelos,
                          bronze_df, silver_clust, silver_fc, config):
    """Construye el HTML ejecutivo premium estilo bento-box."""

    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    version = config.get("project", {}).get("version", "2.0.0")

    # Datos para sector legend
    sector_data = data_payload.get("sector", [])
    sector_html = ""
    if sector_data:
        for s in sector_data:
            sector_html += f"""
            <div class="sector-item">
                <div class="sector-name"><strong>{s['name']}</strong></div>
                <div class="sector-val">Monto: <span class="text-accent">{_fmt_usd(s['monto'])}</span></div>
                <div class="sector-val">Cantidad: {s['cantidad']:,}</div>
                <div class="sector-val">Promedio: {_fmt_usd(s['promedio'])}</div>
            </div>"""

    # Detalle anual HTML rows
    annual_rows = ""
    annual_data = data_payload.get("annual", [])
    for r in annual_data:
        vm = r.get("var_monto")
        vc = r.get("var_cant")
        var_str = ""
        if vm is not None and vc is not None:
            vm_class = "text-green" if vm >= 0 else "text-red"
            vc_class = "text-green" if vc >= 0 else "text-red"
            var_str = f'<span class="{vm_class}">{vm:+.1f}%</span> / <span class="{vc_class}">{vc:+.1f}%</span>'
        annual_rows += f"""<tr>
            <td class="text-bold">{r['year']}</td>
            <td>${r['monto']:,.0f}</td>
            <td>{r['cant']}</td>
            <td>${r['promedio']:,.0f}</td>
            <td>{var_str}</td>
        </tr>\n"""

    # Forecasting tabs
    fc_models = list(forecasting_data.keys())
    fc_tabs_html = ""
    fc_content_html = ""
    for idx, name in enumerate(fc_models):
        active = "active" if idx == 0 else ""
        display = "flex" if idx == 0 else "none"
        fc_tabs_html += f'<button class="fc-tab {active}" onclick="showFcModel(\'{name}\')">{name.upper()}</button>\n'

        # Trayectoria cards
        traj = data_payload.get(f"fc_traj_{name}", [])
        traj_html = ""
        for t in traj:
            g = t.get("growth")
            g_str = f'<span class="{"text-green" if g and g >= 0 else "text-red"}">{g:+.1f}%</span>' if g is not None else ""
            traj_html += f"""<div class="traj-card">
                <div class="traj-year">{t['year']}</div>
                <div class="traj-val">{_fmt_usd(t['value'])}</div>
                <div class="traj-growth">{g_str}</div>
            </div>\n"""

        # Forecast matrix
        matrix = data_payload.get(f"fc_matrix_{name}", [])
        years = sorted(set(k for row in matrix for k in row if k != "Pais"))
        matrix_header = "".join(f"<th>{y}</th>" for y in years)
        matrix_rows = ""
        total_by_year = {y: 0 for y in years}
        for row in matrix:
            cells = ""
            for y in years:
                v = row.get(y, 0)
                total_by_year[y] += v
                cells += f"<td>{_fmt_usd(v)}</td>"
            matrix_rows += f"<tr><td class='text-bold'>{row['Pais']}</td>{cells}</tr>\n"
        # Total row
        total_cells = "".join(f"<td class='text-bold text-accent'>{_fmt_usd(v)}</td>" for v in total_by_year.values())
        matrix_rows += f"<tr class='row-total'><td class='text-bold'>Total General</td>{total_cells}</tr>"

        # Last year close vs projection end
        if traj:
            proj_end = _fmt_usd(traj[-1]["value"]) if traj else "$0"
            proj_start = _fmt_usd(traj[0]["value"]) if traj else "$0"
            total_growth = ((traj[-1]["value"] / traj[0]["value"]) - 1) * 100 if traj and traj[0]["value"] > 0 else 0
        else:
            proj_start = proj_end = "$0"
            total_growth = 0

        fc_content_html += f"""
        <div class="fc-panel" id="fc-{name}" style="display:{display}">
            <div class="fc-layout">
                <div class="fc-sidebar">
                    <div class="kpi-card-sm">
                        <div class="kpi-label">PROYECCIÓN INICIAL</div>
                        <div class="kpi-value-sm">{proj_start}</div>
                    </div>
                    <div class="kpi-card-sm">
                        <div class="kpi-label">PROYECCIÓN FINAL</div>
                        <div class="kpi-value-sm">{proj_end}</div>
                        <div class="kpi-delta {'text-green' if total_growth >= 0 else 'text-red'}">{total_growth:+.1f}%</div>
                    </div>
                    <div class="traj-title">Trayectoria Anual Estimada</div>
                    <div class="traj-container">{traj_html}</div>
                </div>
                <div class="fc-main">
                    <div class="chart-card" style="height:420px">
                        <div id="chart-forecast-{name}" style="width:100%;height:100%"></div>
                    </div>
                    <div class="section-title">Matriz Detallada de Pronósticos</div>
                    <div class="table-wrapper">
                        <table class="exec-table">
                            <thead><tr><th>País</th>{matrix_header}</tr></thead>
                            <tbody>{matrix_rows}</tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>\n"""

    # Clustering tabs
    cl_models = list(clustering_data.keys())
    cl_tabs_html = ""
    cl_content_html = ""
    for idx, name in enumerate(cl_models):
        active = "active" if idx == 0 else ""
        display = "block" if idx == 0 else "none"
        metrics = clustering_data[name].get("metrics", {})
        sil = metrics.get("silhouette", 0) or 0
        k = metrics.get("optimal_k") or metrics.get("n_clusters", "?")
        cl_tabs_html += f'<button class="cl-tab {active}" onclick="showClModel(\'{name}\')">{name.upper()}</button>\n'
        cl_content_html += f"""
        <div class="cl-panel" id="cl-{name}" style="display:{display}">
            <div class="cl-metrics">
                <div class="cl-metric"><span class="cl-metric-val">{sil:.3f}</span><span class="cl-metric-label">Silhouette</span></div>
                <div class="cl-metric"><span class="cl-metric-val">{k}</span><span class="cl-metric-label">Clusters</span></div>
                <div class="cl-metric"><span class="cl-metric-val">{metrics.get('stability_ari', 0) or 0:.2f}</span><span class="cl-metric-label">Estabilidad ARI</span></div>
            </div>
            <div class="chart-card" style="height:400px"><div id="chart-scatter-{name}" style="width:100%;height:100%"></div></div>
        </div>\n"""

    # Comparison table
    comp_rows = ""
    if comparison is not None:
        for _, r in comparison.iterrows():
            comp_rows += f"""<tr>
                <td class="text-bold">{r['modelo'].upper()}</td>
                <td>{r.get('optimal_k', r.get('n_clusters', '—'))}</td>
                <td><span class="badge">{r.get('silhouette', 0):.3f}</span></td>
                <td>{r.get('davies_bouldin', 0):.3f}</td>
                <td>{r.get('calinski_harabasz', 0):,.0f}</td>
                <td>{r.get('stability_ari', 0):.3f}</td>
            </tr>\n"""

    # Charts JSON
    charts_json = json.dumps(charts)

    html = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Ejecutivo BCIE</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
:root {{
    --font: 'Inter', system-ui, sans-serif;
    --bg-body: #0f172a;
    --bg-card: #1e293b;
    --bg-card-alt: #162032;
    --border: rgba(255,255,255,0.08);
    --text-dark: #e2e8f0;
    --text-light: #94a3b8;
    --text-muted: #64748b;
    --primary: #105682;
    --accent: #06b6d4;
    --success: #22c55e;
    --danger: #ef4444;
    --hover: rgba(6,182,212,0.08);
    --radius: 12px;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:var(--font); background:var(--bg-body); color:var(--text-dark); overflow-x:hidden; }}
::-webkit-scrollbar {{ width:6px; height:6px; }}
::-webkit-scrollbar-track {{ background:transparent; }}
::-webkit-scrollbar-thumb {{ background:var(--text-muted); border-radius:3px; }}

/* ── HEADER ── */
.header {{ display:flex; justify-content:space-between; align-items:center; padding:14px 28px; background: linear-gradient(135deg, #0f172a 0%, #1a2744 100%); border-bottom:1px solid var(--border); position:sticky; top:0; z-index:100; }}
.header-left h1 {{ font-size:18px; font-weight:700; color:var(--text-dark); }}
.header-left p {{ font-size:11px; color:var(--text-light); margin-top:2px; }}
.header-right {{ display:flex; align-items:center; gap:12px; }}
.nav-tabs {{ display:flex; gap:4px; background:rgba(255,255,255,0.05); border-radius:8px; padding:3px; }}
.nav-tab {{ padding:7px 16px; border:none; background:transparent; color:var(--text-light); font-family:var(--font); font-size:12px; font-weight:600; cursor:pointer; border-radius:6px; transition:all 0.2s; }}
.nav-tab:hover {{ background:var(--hover); color:var(--text-dark); }}
.nav-tab.active {{ background:var(--primary); color:white; }}
.stamp {{ font-size:10px; color:var(--text-muted); text-align:right; }}

/* ── SECTIONS ── */
.section {{ display:none; padding:20px 28px; min-height:calc(100vh - 56px); }}
.section.active {{ display:block; }}

/* ── BENTO GRID (INICIO) ── */
.bento {{ display:grid; grid-template-columns: 200px 1fr 320px; grid-template-rows: auto auto auto; gap:16px; height:calc(100vh - 96px); }}
.bento > * {{ background:var(--bg-card); border-radius:var(--radius); border:1px solid var(--border); padding:20px; overflow:hidden; }}

/* KPI Cards (izquierda) */
.kpi-stack {{ display:flex; flex-direction:column; gap:16px; grid-row:1/4; justify-content:center; }}
.kpi-item {{ text-align:center; }}
.kpi-label {{ font-size:9px; font-weight:700; letter-spacing:1.2px; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px; }}
.kpi-value {{ font-size:32px; font-weight:800; color:var(--text-dark); line-height:1.1; }}
.kpi-unit {{ font-size:14px; font-weight:400; color:var(--text-light); }}

/* Tabla anual (derecha) */
.annual-panel {{ grid-row:1/4; overflow-y:auto; padding:16px; }}
.annual-title {{ font-size:13px; font-weight:700; color:var(--primary); margin-bottom:12px; }}

/* Charts (centro) */
.chart-card {{ background:var(--bg-card); border-radius:var(--radius); border:1px solid var(--border); padding:16px; overflow:hidden; }}

/* ── TABLES ── */
.exec-table {{ width:100%; border-collapse:collapse; font-size:12px; }}
.exec-table th {{ padding:8px 10px; text-align:left; font-size:10px; font-weight:700; color:var(--primary); text-transform:uppercase; letter-spacing:0.5px; border-bottom:2px solid var(--border); }}
.exec-table td {{ padding:7px 10px; border-bottom:1px solid var(--border); color:var(--text-light); }}
.exec-table tbody tr:hover {{ background:var(--hover); }}
.row-total td {{ background:var(--primary) !important; color:white !important; font-weight:700; }}

/* ── SECTOR SECTION ── */
.sector-grid {{ display:grid; grid-template-columns:1fr auto 1fr; gap:20px; align-items:center; }}
.sector-item {{ margin-bottom:8px; }}
.sector-name {{ font-size:12px; font-weight:600; color:var(--text-dark); }}
.sector-val {{ font-size:11px; color:var(--text-light); }}

/* ── FORECASTING ── */
.fc-tabs {{ display:flex; gap:4px; margin-bottom:16px; background:rgba(255,255,255,0.05); border-radius:8px; padding:3px; width:fit-content; }}
.fc-tab {{ padding:7px 18px; border:none; background:transparent; color:var(--text-light); font-family:var(--font); font-size:12px; font-weight:600; cursor:pointer; border-radius:6px; transition:all 0.2s; }}
.fc-tab:hover {{ background:var(--hover); }}
.fc-tab.active {{ background:var(--primary); color:white; }}
.fc-layout {{ display:grid; grid-template-columns:220px 1fr; gap:16px; }}
.fc-sidebar {{ display:flex; flex-direction:column; gap:12px; }}
.fc-main {{ display:flex; flex-direction:column; gap:16px; }}
.kpi-card-sm {{ background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius); padding:16px; text-align:center; }}
.kpi-value-sm {{ font-size:22px; font-weight:800; color:var(--text-dark); }}
.kpi-delta {{ font-size:14px; font-weight:600; margin-top:4px; }}
.traj-title {{ font-size:12px; font-weight:700; color:var(--primary); margin-top:8px; }}
.traj-container {{ display:flex; flex-direction:column; gap:8px; overflow-y:auto; }}
.traj-card {{ background:var(--bg-card-alt); border:1px solid var(--border); border-radius:8px; padding:10px 12px; transition:all 0.2s; cursor:default; }}
.traj-card:hover {{ border-color:var(--primary); transform:translateX(3px); }}
.traj-year {{ font-size:12px; font-weight:700; color:var(--text-light); }}
.traj-val {{ font-size:16px; font-weight:800; color:var(--text-dark); }}
.traj-growth {{ font-size:12px; font-weight:600; }}

/* ── CLUSTERING ── */
.cl-tabs {{ display:flex; gap:4px; margin-bottom:16px; flex-wrap:wrap; background:rgba(255,255,255,0.05); border-radius:8px; padding:3px; width:fit-content; }}
.cl-tab {{ padding:6px 14px; border:none; background:transparent; color:var(--text-light); font-family:var(--font); font-size:11px; font-weight:600; cursor:pointer; border-radius:6px; transition:all 0.2s; }}
.cl-tab:hover {{ background:var(--hover); }}
.cl-tab.active {{ background:var(--primary); color:white; }}
.cl-metrics {{ display:flex; gap:16px; margin-bottom:16px; }}
.cl-metric {{ background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:12px 20px; text-align:center; flex:1; }}
.cl-metric-val {{ font-size:24px; font-weight:800; color:var(--accent); display:block; }}
.cl-metric-label {{ font-size:10px; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; }}

/* ── UTILITIES ── */
.text-bold {{ font-weight:700; color:var(--text-dark); }}
.text-accent {{ color:var(--accent); }}
.text-green {{ color:var(--success); font-weight:600; }}
.text-red {{ color:var(--danger); font-weight:600; }}
.badge {{ background:rgba(6,182,212,0.15); color:var(--accent); padding:2px 8px; border-radius:4px; font-weight:700; font-size:12px; }}
.section-title {{ font-size:14px; font-weight:700; color:var(--text-dark); margin:8px 0; }}
.table-wrapper {{ background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius); padding:16px; overflow-x:auto; }}
.toggle-group {{ display:flex; gap:8px; align-items:center; }}
.toggle-group label {{ font-size:10px; color:var(--text-light); cursor:pointer; }}

/* ── FOOTER ── */
.footer {{ text-align:center; padding:16px; font-size:10px; color:var(--text-muted); border-top:1px solid var(--border); }}

/* ── RESPONSIVE ── */
@media (max-width: 1200px) {{
    .bento {{ grid-template-columns:1fr; grid-template-rows:auto; }}
    .kpi-stack {{ flex-direction:row; grid-row:auto; }}
    .annual-panel {{ grid-row:auto; max-height:300px; }}
    .fc-layout {{ grid-template-columns:1fr; }}
}}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
    <div class="header-left">
        <h1>Dashboard Ejecutivo BCIE</h1>
        <p>Análisis Integral de Aprobaciones Históricas (Datos Reales)</p>
    </div>
    <div class="header-right">
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showSection('inicio')">Inicio</button>
            <button class="nav-tab" onclick="showSection('forecasting')">Forecasting</button>
            <button class="nav-tab" onclick="showSection('clustering')">Clustering</button>
            <button class="nav-tab" onclick="showSection('comparativa')">Comparativa</button>
        </div>
        <div class="stamp">Datos Actualizados: {now}</div>
    </div>
</div>

<!-- ═══════════ INICIO ═══════════ -->
<div class="section active" id="sec-inicio">
    <div class="bento">
        <!-- KPIs (columna izquierda) -->
        <div class="kpi-stack">
            <div class="kpi-item">
                <div class="kpi-label">Monto Total Aprobado</div>
                <div class="kpi-value">USD {total_monto:,.0f}</div>
            </div>
            <div class="kpi-item">
                <div class="kpi-label">Cantidad de Aprobaciones</div>
                <div class="kpi-value">{total_aprobaciones:,}</div>
            </div>
            <div class="kpi-item">
                <div class="kpi-label">Promedio por Aprobación</div>
                <div class="kpi-value">USD {(total_monto / max(total_aprobaciones, 1)):,.0f}</div>
            </div>
        </div>

        <!-- Evolución Temporal (centro arriba) -->
        <div class="chart-card" style="grid-column:2; grid-row:1/2">
            <div id="chart-evolucion" style="width:100%;height:100%"></div>
        </div>

        <!-- Tabla Detalle Anual (derecha) -->
        <div class="annual-panel">
            <div class="annual-title">Detalle Anual</div>
            <table class="exec-table">
                <thead>
                    <tr><th>Año</th><th>Monto</th><th>Cant.</th><th>Promedio por Aprobación</th><th>Var. YoY</th></tr>
                </thead>
                <tbody>{annual_rows}</tbody>
            </table>
        </div>

        <!-- Distribución Sector (centro izquierda) -->
        <div class="chart-card" style="grid-column:2; grid-row:2">
            <div class="section-title">Distribución por Sector Institucional</div>
            <div class="sector-grid">
                <div id="chart-donut-monto" style="width:100%;height:220px"></div>
                <div class="sector-legend">{sector_html}</div>
                <div id="chart-donut-cant" style="width:100%;height:220px"></div>
            </div>
        </div>

        <!-- Participación por País (abajo centro) -->
        <div class="chart-card" style="grid-column:1/3; grid-row:3">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div class="section-title">Participación por País</div>
            </div>
            <div id="chart-pais-bars" style="width:100%;height:280px"></div>
        </div>

        <!-- Tipo de Socio (abajo derecha) -->
        <div class="chart-card" style="grid-row:3">
            <div class="section-title">Por Tipo de Socio</div>
            <div id="chart-tipo-socio" style="width:100%;height:180px"></div>
        </div>
    </div>
</div>

<!-- ═══════════ FORECASTING ═══════════ -->
<div class="section" id="sec-forecasting">
    <div class="section-title" style="font-size:16px;margin-bottom:12px;">Análisis de Proyección de Aprobaciones del BCIE</div>
    <div class="fc-tabs">{fc_tabs_html}</div>
    {fc_content_html}
</div>

<!-- ═══════════ CLUSTERING ═══════════ -->
<div class="section" id="sec-clustering">
    <div class="section-title" style="font-size:16px;margin-bottom:12px;">Modelos de Clustering</div>
    <div class="cl-tabs">{cl_tabs_html}</div>
    {cl_content_html}
</div>

<!-- ═══════════ COMPARATIVA ═══════════ -->
<div class="section" id="sec-comparativa">
    <div class="section-title" style="font-size:16px;margin-bottom:12px;">Comparativa de Modelos de Clustering</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
        <div class="chart-card" style="height:440px">
            <div id="chart-radar" style="width:100%;height:100%"></div>
        </div>
        <div class="table-wrapper">
            <table class="exec-table">
                <thead><tr><th>Modelo</th><th>K</th><th>Silhouette</th><th>Davies-Bouldin</th><th>Calinski-H.</th><th>Estabilidad</th></tr></thead>
                <tbody>{comp_rows}</tbody>
            </table>
        </div>
    </div>
</div>

<!-- FOOTER -->
<div class="footer">
    Este tablero presenta datos reales obtenidos del portal de datos abiertos del BCIE.
    &copy; {datetime.now().year} Dashboard Ejecutivo v{version} &mdash; Norman Sabillón | Analista de Datos
</div>

<script>
// Charts data
const CHARTS = {charts_json};

// Navigation
function showSection(id) {{
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('sec-' + id).classList.add('active');
    event.target.classList.add('active');
    // Re-render charts in the section
    setTimeout(() => renderAll(), 50);
}}

// Forecasting model tabs
function showFcModel(name) {{
    document.querySelectorAll('.fc-panel').forEach(p => p.style.display = 'none');
    document.querySelectorAll('.fc-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('fc-' + name).style.display = 'flex';
    event.target.classList.add('active');
    setTimeout(() => {{
        const el = document.getElementById('chart-forecast-' + name);
        if (el && CHARTS['forecast_' + name]) {{
            Plotly.react(el, JSON.parse(CHARTS['forecast_' + name]).data, JSON.parse(CHARTS['forecast_' + name]).layout, {{responsive:true}});
        }}
    }}, 50);
}}

// Clustering model tabs
function showClModel(name) {{
    document.querySelectorAll('.cl-panel').forEach(p => p.style.display = 'none');
    document.querySelectorAll('.cl-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('cl-' + name).style.display = 'block';
    event.target.classList.add('active');
    setTimeout(() => {{
        const el = document.getElementById('chart-scatter-' + name);
        if (el && CHARTS['scatter_' + name]) {{
            Plotly.react(el, JSON.parse(CHARTS['scatter_' + name]).data, JSON.parse(CHARTS['scatter_' + name]).layout, {{responsive:true}});
        }}
    }}, 50);
}}

// Render all visible charts
function renderAll() {{
    for (const [key, json_str] of Object.entries(CHARTS)) {{
        let el_id = 'chart-' + key.replace('_', '-').replace('_', '-');
        // Map chart keys to element IDs
        const mappings = {{
            'evolucion': 'chart-evolucion',
            'donut_monto': 'chart-donut-monto',
            'donut_cant': 'chart-donut-cant',
            'pais_bars': 'chart-pais-bars',
            'tipo_socio': 'chart-tipo-socio',
            'radar': 'chart-radar',
        }};
        if (mappings[key]) el_id = mappings[key];
        else if (key.startsWith('forecast_')) el_id = 'chart-forecast-' + key.replace('forecast_', '');
        else if (key.startsWith('scatter_')) el_id = 'chart-scatter-' + key.replace('scatter_', '');
        else continue;

        const el = document.getElementById(el_id);
        if (el && el.offsetParent !== null) {{
            try {{
                const parsed = JSON.parse(json_str);
                Plotly.react(el, parsed.data, parsed.layout, {{responsive:true, displayModeBar:false}});
            }} catch(e) {{ console.warn('Chart error:', key, e); }}
        }}
    }}
}}

// Initial render
window.addEventListener('load', () => {{ renderAll(); }});
window.addEventListener('resize', () => {{ renderAll(); }});
</script>
</body>
</html>"""
    return html
