import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import numpy as np

POSITIVE_WORDS = ["menguat", "menghijau", "naik", "laba", "tumbuh", "lonjakan", "cemerlang", "rekor", "prospek", "positif", "terbang"]
NEGATIVE_WORDS = ["anjlok", "merah", "turun", "rugi", "tekanan", "melemah", "koreksi", "anomali", "negatif", "pangkas", "longsor"]

SECTOR_PROXIES = {
    "Teknologi": "GOTO.JK",
    "Keuangan": "BBCA.JK",
    "Energi": "ADRO.JK",
    "Kesehatan": "KLBF.JK",
    "Infrastruktur": "TLKM.JK"
}

def analyze_sentiment(text):
    text_lower = text.lower()
    pos_score = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    neg_score = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    
    if pos_score > neg_score:
        return 100
    elif neg_score > pos_score:
        return 0
    else:
        return 50

def fetch_financial_news():
    url = "https://news.google.com/rss/search?q=saham+indonesia+sektor&hl=id&gl=ID&ceid=ID:id"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all("item", limit=5)
    
    news_list = []
    sentiments = []
    for item in items:
        title = item.title.text
        score = analyze_sentiment(title)
        sentiments.append(score)
        
        label = "Positif 🟢" if score == 100 else ("Negatif 🔴" if score == 0 else "Netral 🟡")
        news_list.append({
            "Judul Berita": title,
            "Hasil Sentimen NLP": label,
            "Tanggal": item.pubDate.text,
            "Sumber": item.source.text if item.source else "Google News"
        })
        
    avg_news_score = sum(sentiments) / len(sentiments) if sentiments else 50
    return pd.DataFrame(news_list), avg_news_score

def fetch_quantitative_scores():
    quant_scores = {}
    for sector, ticker in SECTOR_PROXIES.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            # Membersihkan data kosong (NaN) dari baris harga Close
            hist_close = hist['Close'].dropna()
            
            if len(hist_close) >= 2:
                price_start = float(hist_close.iloc[0])
                price_end = float(hist_close.iloc[-1])
                
                if price_start > 0:
                    pct_change = ((price_end - price_start) / price_start) * 100
                    score = min(max(50 + (pct_change * 5), 0), 100)
                    
                    if np.isnan(score):
                        quant_scores[sector] = 50.0
                    else:
                        quant_scores[sector] = round(float(score), 1)
                else:
                    quant_scores[sector] = 50.0
            else:
                quant_scores[sector] = 50.0
        except Exception:
            quant_scores[sector] = 50.0
            
    return quant_scores

def get_sector_data(news_score):
    quant_scores = fetch_quantitative_scores()
    
    sector_rows = []
    for sector in SECTOR_PROXIES.keys():
        q_score = quant_scores.get(sector, 50.0)
        if np.isnan(q_score) or q_score is None:
            q_score = 50.0
            
        final_score = round((0.30 * news_score) + (0.70 * q_score), 1)
        
        sector_rows.append({
            "Sektor": sector,
            "Proxy Ticker": SECTOR_PROXIES[sector],
            "Skor Sentimen Berita (30%)": round(news_score, 1),
            "Skor Tren Kuantitatif (70%)": q_score,
            "Skor Akhir Hybrid": final_score
        })
        
    df = pd.DataFrame(sector_rows)
    return df.sort_values(by="Skor Akhir Hybrid", ascending=False)