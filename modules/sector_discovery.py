import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_financial_news():
    """
    Mengambil judul berita ekonomi/saham terbaru dari Google News RSS (Bahasa Indonesia).
    """
    url = "https://news.google.com/rss/search?q=saham+indonesia+sektor&hl=id&gl=ID&ceid=ID:id"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features="xml")
    
    items = soup.find_all("item", limit=5)
    
    news_list = []
    for item in items:
        news_list.append({
            "Judul Berita": item.title.text,
            "Tanggal": item.pubDate.text,
            "Sumber": item.source.text if item.source else "Google News"
        })
        
    return pd.DataFrame(news_list)

def get_sector_data():
    """
    Data ringkasan sektor saham Indonesia.
    """
    data = {
        "Sektor": ["Teknologi", "Keuangan", "Energi", "Kesehatan", "Infrastruktur"],
        "Sentimen Sektor": ["Positif", "Sangat Positif", "Netral", "Positif", "Netral"],
        "Skor AI (0-100)": [78, 88, 52, 70, 58]
    }
    return pd.DataFrame(data)