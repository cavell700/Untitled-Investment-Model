import pandas as pd
import requests
from bs4 import BeautifulSoup

# Daftar kata kunci finansial untuk deteksi sentimen dasar
POSITIVE_WORDS = ["menguat", "menghijau", "naik", "laba", "tumbuh", "lonjakan", "cemerlang", "rekor", "prospek", "positif", "terbang"]
NEGATIVE_WORDS = ["anjlok", "merah", "turun", "rugi", "tekanan", "melemah", "koreksi", "anomali", "negatif", "pangkas", "longsor"]

def analyze_sentiment(text):
    """
    Menganalisis teks berita menggunakan kamus istilah finansial dasar.
    """
    text_lower = text.lower()
    pos_score = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    neg_score = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    
    if pos_score > neg_score:
        return "Positif 🟢"
    elif neg_score > pos_score:
        return "Negatif 🔴"
    else:
        return "Netral 🟡"

def fetch_financial_news():
    """
    Scrape berita dari Google News RSS & memproses sentimennya.
    """
    url = "https://news.google.com/rss/search?q=saham+indonesia+sektor&hl=id&gl=ID&ceid=ID:id"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features="xml")
    
    items = soup.find_all("item", limit=5)
    
    news_list = []
    for item in items:
        title = item.title.text
        sentiment = analyze_sentiment(title)
        news_list.append({
            "Judul Berita": title,
            "Hasil Sentimen NLP": sentiment,
            "Tanggal": item.pubDate.text,
            "Sumber": item.source.text if item.source else "Google News"
        })
        
    return pd.DataFrame(news_list)

def get_sector_data():
    """
    Simulasi tabel pembobotan Hybrid Scoring (30% Berita + 70% Tren Kuantitatif).
    """
    data = {
        "Sektor": ["Teknologi", "Keuangan", "Energi", "Kesehatan", "Infrastruktur"],
        "Skor Sentimen Berita (30%)": [70, 90, 40, 75, 50],
        "Skor Tren Kuantitatif (70%)": [81, 87, 57, 68, 61],
        "Skor Akhir Hybrid": [77.7, 87.9, 51.9, 70.1, 57.7]
    }
    return pd.DataFrame(data)