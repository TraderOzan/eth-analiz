import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(page_title="ETH Veri Analizi", layout="wide")

st.title("📊 Ethereum On-Chain & Fiyat Analiz Paneli")
st.markdown("Bir Matematikçi Gözüyle Zaman Serisi Analizi")

# Yan Panel (Sidebar) Ayarları
st.sidebar.header("Parametreleri Ayarla")
ticker = "ETH-USD"
period = st.sidebar.selectbox("Zaman Aralığı", ["1mo", "3mo", "6mo", "1y", "2y"])
ma_window = st.sidebar.slider("Hareketli Ortalama Penceresi (Gün)", 5, 50, 20)

# Veri Çekme
@st.cache_data # Veriyi her seferinde tekrar indirmemek için önbelleğe alır
def data_load(p):
    df = yf.download(ticker, period=p)
    df.columns = df.columns.get_level_values(0)
    return df

data = data_load(period)

# Hesaplamalar
data['MA'] = data['Close'].rolling(window=ma_window).mean()
data['Volatility'] = data['Close'].rolling(window=ma_window).std()

# Grafik Oluşturma (Plotly ile Interaktif)
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="ETH Fiyat", line=dict(color='cyan')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA'], name=f"{ma_window} Günlük MA", line=dict(color='orange', dash='dot')))

fig.update_layout(title="Ethereum Fiyat ve Hareketli Ortalama", template="plotly_dark", xaxis_title="Tarih", yaxis_title="Fiyat (USD)")

# Dashboard Arayüzü
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("İstatistiksel Özet")
    st.write(data[['Close', 'Volatility']].tail(10))
    st.metric("Güncel Fiyat", f"${data['Close'].iloc[-1]:.2f}")
    st.metric("Volatilite (Standart Sapma)", f"{data['Volatility'].iloc[-1]:.2f}")

st.info("Bu panel, verideki gürültüyü (noise) temizlemek için hareketli ortalama filtresi kullanmaktadır.")