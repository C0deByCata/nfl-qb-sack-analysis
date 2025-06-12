"""Main module for the NFL Sacks Analysis Streamlit app."""

import os
import streamlit as st
import plotly.express as px
import plotly.io as pio
from core.data import load_data
from core.plots import (
    PALETTE,
    bar_avg_sacks_losses,
    scatter_sacks_vs_points,
    box_sacks_distribution,
    corr_heatmap,
    scatter_sacks_vs_margin,
)


_dark = pio.templates["plotly_dark"].layout.template
pio.templates["darkCustom"] = _dark
pio.templates["darkCustom"].layout.paper_bgcolor = PALETTE["neutral"]
pio.templates["darkCustom"].layout.plot_bgcolor = PALETTE["neutral"]
pio.templates.default = "darkCustom"


st.set_page_config(
    page_title="NFL Sacks Analysis", layout="wide", initial_sidebar_state="expanded"
)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "processed_data.csv")
df_raw = load_data(data_path)

st.sidebar.header("Filtros")
season = st.sidebar.selectbox(
    "Temporada", sorted(df_raw["season"].unique(), reverse=True)
)
phase_sel = st.sidebar.multiselect(
    "Fase", sorted(df_raw["phase"].unique()), default=sorted(df_raw["phase"].unique())
)
all_teams = st.sidebar.checkbox("Todos los equipos", value=True)
team_sel = (
    sorted(df_raw["team_abbr"].unique())
    if all_teams
    else st.sidebar.multiselect("Equipos", sorted(df_raw["team_abbr"].unique()))
)
resultado = st.sidebar.radio("Resultado", ["all", "win", "loss"], horizontal=True)
min_sacks = st.sidebar.slider(
    "Sacks permitidos mínimos",
    int(df_raw["sacks_permitidos"].min()),
    int(df_raw["sacks_permitidos"].max()),
    0,
)
method = st.sidebar.radio(
    "Método correlación", ["pearson", "spearman", "kendall"], horizontal=True
)


mask = (
    (df_raw["season"] == season)
    & (df_raw["phase"].isin(phase_sel))
    & (df_raw["team_abbr"].isin(team_sel if team_sel else df_raw["team_abbr"]))
    & (df_raw["sacks_permitidos"] >= min_sacks)
)
df_f = df_raw[mask].copy()
df_o = df_f if resultado == "all" else df_f[df_f["resultado"] == resultado]


st.title("NFL Sacks Analysis – margen ≥ 8 pts")
st.write(
    f"**Temporada:** {season}  |  **Fases:** {', '.join(phase_sel)}  |  "
    f"**Equipos:** {'Todos' if all_teams else ', '.join(team_sel)}"
)


st.subheader("1 · Sacks promedio en derrotas")
st.plotly_chart(bar_avg_sacks_losses(df_f), use_container_width=True)


st.subheader("2 · Sacks vs puntos anotados")
if not df_o.empty:
    if all_teams or len(team_sel) > 1:
        fig2 = scatter_sacks_vs_points(
            df_o,
            "team_abbr",
            "phase",
            {"color_discrete_sequence": px.colors.qualitative.Safe},
            "overall",
        )
    else:
        fig2 = scatter_sacks_vs_points(
            df_o,
            "phase",
            "resultado",
            {
                "color_discrete_map": {
                    "regular": PALETTE["primary"],
                    "playoff": PALETTE["secondary"],
                }
            },
            "trace",
        )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No hay datos con los filtros actuales.")


st.subheader("3 · Distribución de sacks")
st.plotly_chart(
    box_sacks_distribution(df_o, all_teams or len(team_sel) > 1),
    use_container_width=True,
)

st.subheader("4 · Matriz de correlaciones")
num_cols = ["sacks_permitidos", "pct_sacks", "margin", "puntos_anotados"]
st.plotly_chart(corr_heatmap(df_f, num_cols, method), use_container_width=True)


st.subheader("5 · Top-10 partidos con más sacks")
top10 = df_f.sort_values("sacks_permitidos", ascending=False).head(10)
st.dataframe(
    top10[
        [
            "season",
            "week",
            "partido_id",
            "local_team_name",
            "visitante_team_name",
            "sacks_permitidos",
        ]
    ],
    use_container_width=True,
)


st.subheader("6 · Sacks vs margen (scatter)")
st.plotly_chart(scatter_sacks_vs_margin(df_o), use_container_width=True)
