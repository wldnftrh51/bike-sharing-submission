from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    day = pd.read_csv(BASE_DIR / "day_clean.csv", parse_dates=["dateday"])
    hour = pd.read_csv(BASE_DIR / "hour_clean.csv", parse_dates=["dateday"])
    return day, hour

day, hour = load_data()
st.title("Bike Sharing Dashboard")
st.caption("Ringkasan pola penyewaan sepeda berdasarkan data harian dan per jam.")

with st.sidebar:
    st.header("Filter")
    dataset_choice = st.radio("Granularitas data", ["Harian", "Per jam"])
    source = day if dataset_choice == "Harian" else hour
    min_date, max_date = source["dateday"].min().date(), source["dateday"].max().date()
    date_range = st.date_input("Rentang tanggal", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    seasons = sorted(source["season"].dropna().unique().tolist())
    selected_seasons = st.multiselect("Musim", seasons, default=seasons)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range
filtered = source[(source["dateday"].dt.date >= start_date) & (source["dateday"].dt.date <= end_date)]
filtered = filtered[filtered["season"].isin(selected_seasons)]

if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total penyewaan", f"{filtered['count'].sum():,}")
col2.metric("Pengguna casual", f"{filtered['casual'].sum():,}")
col3.metric("Pengguna terdaftar", f"{filtered['registered'].sum():,}")

left, right = st.columns(2)
with left:
    st.subheader("Total penyewaan menurut musim")
    season_totals = filtered.groupby("season", observed=False)["count"].sum().reindex(["Spring", "Summer", "Autumn", "Winter"]).dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    season_totals.plot(kind="bar", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total penyewaan")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
with right:
    st.subheader("Total penyewaan menurut kondisi cuaca")
    weather_totals = filtered.groupby("weathersit")["count"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    weather_totals.plot(kind="bar", ax=ax)
    ax.set_xlabel("Kondisi cuaca")
    ax.set_ylabel("Total penyewaan")
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

if dataset_choice == "Per jam":
    st.subheader("Pola penyewaan menurut jam")
    hourly = filtered.groupby("hour")["count"].sum().reindex(range(24), fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 4))
    hourly.plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Total penyewaan")
    ax.set_xticks(range(24))
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.subheader("Total penyewaan menurut hari dalam seminggu")
    weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekday_totals = filtered.groupby("weekday")["count"].sum().reindex(weekday_order).dropna()
    fig, ax = plt.subplots(figsize=(10, 4))
    weekday_totals.plot(kind="bar", ax=ax)
    ax.set_xlabel("Hari")
    ax.set_ylabel("Total penyewaan")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Data hasil filter")
st.dataframe(filtered, use_container_width=True)
st.download_button("Unduh data hasil filter (CSV)", filtered.to_csv(index=False).encode("utf-8"), file_name="bike_sharing_filtered.csv", mime="text/csv")
