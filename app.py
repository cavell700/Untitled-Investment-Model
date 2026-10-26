import streamlit as st
from modules.sector_discovery import get_sector_data, fetch_financial_news

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
st.header("🔍 Modul 1: Sector Discovery Engine (Hybrid Approach)")
st.write("Hasil kalkulasi peringkat sektor saham berdasarkan **Hybrid Scoring** (30% Sentimen NLP + 70% Data Tren Pasar):")

# Tampilkan Skor Hybrid Sektor
df_sektor = get_sector_data()
st.dataframe(df_sektor, use_container_width=True)

st.subheader("📰 Berita Sentimen Pasar Terbaru & Analisis NLP")

# Caching data berita selama 1 jam (3600 detik) agar antarmuka tidak mendadak loading saat diklik
@st.cache_data(ttl=3600)
def load_cached_news():
    return fetch_financial_news()

with st.spinner("Mengambil berita & menganalisis sentimen teks..."):
    df_berita = load_cached_news()
    st.dataframe(df_berita, use_container_width=True)