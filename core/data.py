"""Module for the NFL Sacks App."""

import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Carga el CSV principal y calcula columnas auxiliares."""
    df = pd.read_csv(path, parse_dates=["fecha"])
    if "week" not in df.columns:
        df["week"] = df["fecha"].dt.isocalendar().week
    if "loc_vi" not in df.columns:
        df["loc_vi"] = df["is_home"].map({True: "Casa", False: "Visitante"})
    return df
