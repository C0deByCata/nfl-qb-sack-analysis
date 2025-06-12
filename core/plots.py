"""Module for generating various plots related to NFL sacks data."""

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import scipy.cluster.hierarchy as sch
import pandas as pd

PALETTE = {  # paleta global, reutilizada
    "primary": "#1B6EF3",
    "secondary": "#FF9803",
    "accent": "#1CC29F",
    "danger": "#E02945",
    "neutral": "#9E9E9E",
}


def bar_avg_sacks_losses(df: pd.DataFrame) -> go.Figure:
    """Genera un gráfico de barras que muestra el promedio de sacks permitidos por equipo en partidos perdidos.

    Args:
        df (pd.DataFrame): DataFrame con los datos de partidos.

    Returns:
        go.Figure: Gráfico de barras con el promedio de sacks permitidos.
    """
    loss_df = df[df["resultado"] == "loss"]
    avg = (
        loss_df.groupby("team_abbr")["sacks_permitidos"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    return px.bar(
        avg,
        x="team_abbr",
        y="sacks_permitidos",
        color_discrete_sequence=[PALETTE["danger"]],
        labels={"team_abbr": "Equipo", "sacks_permitidos": "Sacks promedio"},
        title="Sacks promedio en derrotas",
    )


def scatter_sacks_vs_points(
    df: pd.DataFrame,
    color_col: str,
    symbol_col: str,
    color_args: dict,
    trend_scope: str,
) -> go.Figure:
    """Genera un gráfico de dispersión que muestra la relación entre sacks permitidos y puntos anotados.

    Args:
        df (pd.DataFrame): DataFrame con los datos de partidos.
        color_col (str): Nombre de la columna para el color de los puntos.
        symbol_col (str): Nombre de la columna para el símbolo de los puntos.
        color_args (dict): Argumentos adicionales para el color.
        trend_scope (str): Alcance de la línea de tendencia.

    Returns:
        go.Figure: Gráfico de dispersión con la relación entre sacks y puntos anotados.
    """
    return px.scatter(
        df,
        x="sacks_permitidos",
        y="puntos_anotados",
        color=color_col,
        symbol=symbol_col,
        trendline="ols",
        trendline_scope=trend_scope,
        labels={
            "sacks_permitidos": "Sacks recibidos",
            "puntos_anotados": "Puntos anotados",
            color_col: color_col.replace("_", " ").title(),
        },
        hover_data=["partido_id", "week", "phase", "resultado"],
        title="Sacks vs Puntos anotados",
        **color_args,
    )


def box_sacks_distribution(df: pd.DataFrame, group_by_team: bool = True) -> go.Figure:
    """Genera un gráfico de caja que muestra la distribución de sacks permitidos por equipo o por resultado.

    Args:
        df (pd.DataFrame): DataFrame con los datos de partidos.
        group_by_team (bool, optional): Agrupar por equipo si es True, por resultado si es False. Defaults to True.

    Returns:
        go.Figure: Gráfico de caja con la distribución de sacks permitidos.
    """
    if group_by_team:
        return px.box(
            df,
            x="team_abbr",
            y="sacks_permitidos",
            color="resultado",
            color_discrete_map={"win": PALETTE["accent"], "loss": PALETTE["danger"]},
            title="Sacks por equipo y resultado",
            labels={"team_abbr": "Equipo", "sacks_permitidos": "Sacks recibidos"},
        )
    return px.box(
        df,
        x="resultado",
        y="sacks_permitidos",
        color="resultado",
        color_discrete_map={"win": PALETTE["accent"], "loss": PALETTE["danger"]},
        title="Sacks en victorias vs derrotas",
        labels={"resultado": "Resultado", "sacks_permitidos": "Sacks recibidos"},
    )


def corr_heatmap(df: pd.DataFrame, numeric_cols: list, method: str) -> go.Figure:
    """Genera un mapa de calor de correlaciones entre columnas numéricas del DataFrame.

    Args:
        df (pd.DataFrame): DataFrame con los datos.
        numeric_cols (list): Lista de nombres de columnas numéricas a incluir en el cálculo de correlaciones.
        method (str): Método de correlación a utilizar ('pearson', 'spearman', 'kendall').

    Returns:
        go.Figure: Mapa de calor de correlaciones entre columnas numéricas.
    """
    corr = df[numeric_cols].corr(method=method, numeric_only=True)
    if len(numeric_cols) > 2:
        linkage = sch.linkage(corr, method="average")
        order = sch.dendrogram(linkage, no_plot=True)["leaves"]
        corr = corr.iloc[order, order]
    mask = np.triu(np.ones_like(corr, dtype=bool))
    return px.imshow(
        corr.mask(mask),
        zmin=-1,
        zmax=1,
        text_auto=".2f",
        aspect="auto",
        origin="lower",
        color_continuous_scale=[
            [0, PALETTE["danger"]],
            [0.5, "#202020"],
            [1, PALETTE["accent"]],
        ],
        title=f"Correlaciones ({method.title()})",
    )


def scatter_sacks_vs_margin(df: pd.DataFrame) -> go.Figure:
    """Genera un gráfico de dispersión que muestra la relación entre sacks permitidos y margen de victoria/derrota.
    Args:
        df (pd.DataFrame): DataFrame con los datos de partidos.
    Returns:
        go.Figure: Gráfico de dispersión con la relación entre sacks y margen.
    """
    colors = {"win": PALETTE["accent"], "loss": PALETTE["danger"]}
    fig = px.scatter(
        df,
        x="sacks_permitidos",
        y="margin",
        color="resultado",
        symbol="resultado",
        color_discrete_map=colors,
        labels={
            "sacks_permitidos": "Sacks permitidos",
            "margin": "Margen (+ gana / – pierde)",
        },
        hover_data=["partido_id", "week", "team_abbr"],
        title="Sacks permitidos vs margen (≥ 8 pts)",
        trendline="ols",
        trendline_scope="overall",
    )
    fig.add_hline(y=0, line_dash="dot", line_color=PALETTE["neutral"])
    return fig
