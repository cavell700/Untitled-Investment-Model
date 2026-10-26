import streamlit as st
from modules.sector_discovery import get_sector_data, fetch_financial_news

st.set_page_config(
    page_title="AI Investment Model",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Investment & Stock Picker Model")
st.subheader("Model Prediksi Prospek Saham Indonesia berbasis NLP & Valuasi Keuangan")

st.divider()

st.header("🔍 Modul 1: Sector Discovery Engine (Hybrid Approach)")
st.write("Hasil kalkulasi peringkat sektor saham berdasarkan **Data Real Pasar** (30% Sentimen NLP + 70% Tren Harga Real):")

@st.cache_data(ttl=3600)
def load_cached_data():
    df_berita, avg_news_score = fetch_financial_news()
    df_sektor = get_sector_data(avg_news_score)
    return df_berita, df_sektor

with st.spinner("Mengambil data berita & harga saham real pasar..."):
    df_berita, df_sektor = load_cached_data()
    
    st.subheader("🏆 Peringkat Sektor Prospektif")
    st.dataframe(df_sektor, use_container_width=True)
    
    st.subheader("📰 Berita Sentimen Pasar Terbaru & Analisis NLP")
    st.dataframe(df_berita, use_container_width=True)