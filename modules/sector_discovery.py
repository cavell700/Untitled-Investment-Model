import pandas as pd

def get_sector_data():
    """
    Fungsi sementara untuk menyimulasikan data analisis sektor saham.
    Nanti fungsi ini akan kita hubungkan dengan Scraper Berita & IndoBERT.
    """
    data = {
        "Sektor": ["Teknologi", "Keuangan", "Energi", "Kesehatan", "Infrastruktur"],
        "Sentimen Sektor": ["Positif", "Sangat Positif", "Netral", "Positif", "Netral"],
        "Skor AI (0-100)": [78, 88, 52, 70, 58]
    }
    return pd.DataFrame(data)