import streamlit as st
from modules.sector_discovery import get_sector_data

# Konfigurasi Halaman
st.set_page_config(
    page_title="AI Investment Model",
    page_icon="📈",
    layout="wide"
)

# Judul Utama
st.title("📈 AI Investment & Stock Picker Model")
st.subheader("Model Prediksi Prospek Saham Indonesia berbasis NLP & Valuasi Keuangan")

st.divider()

# Modul 1: Sector Discovery Engine
st.header("🔍 Modul 1: Sector Discovery Engine")
st.write("Analisis tren dan sentimen sektor industri saham di Indonesia saat ini:")

# Panggil data dari modules
df_sektor = get_sector_data()
st.dataframe(df_sektor, use_container_width=True)