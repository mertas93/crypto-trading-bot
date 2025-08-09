#!/usr/bin/env python3
"""
Debug test - en basit
"""
import requests
import time

def test_api():
    print("🧪 API Test başlıyor...")
    
    # 1. CoinGecko test
    try:
        print("1️⃣ CoinGecko test...")
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {'vs_currency': 'usd', 'days': '1', 'interval': 'hourly'}
        
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            prices = data.get('prices', [])
            print(f"   ✅ {len(prices)} fiyat verisi alındı")
            if prices:
                print(f"   Son fiyat: ${prices[-1][1]:.2f}")
        
    except Exception as e:
        print(f"   ❌ Hata: {e}")
    
    # 2. Binance test
    try:
        print("2️⃣ Binance test...")
        url = "https://api.binance.com/api/v3/klines"
        params = {
            'symbol': 'BTCUSDT',
            'interval': '1h',
            'limit': 24
        }
        
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {len(data)} candle verisi alındı")
            if data:
                close_price = float(data[-1][4])
                print(f"   Son kapanış: ${close_price:.2f}")
        
    except Exception as e:
        print(f"   ❌ Hata: {e}")

def test_analysis():
    print("\n📊 Analiz test...")
    
    # Fake data ile analiz test
    fake_prices = [50000, 50100, 50200, 50150, 50300, 50250, 50400, 50350, 50500, 50450] * 5
    print(f"   Fake data: {len(fake_prices)} fiyat")
    
    # Basit MA hesapla
    import numpy as np
    ma5 = np.mean(fake_prices[-5:])
    ma10 = np.mean(fake_prices[-10:])
    
    print(f"   MA5: ${ma5:.2f}")
    print(f"   MA10: ${ma10:.2f}")
    print("   ✅ Analiz çalışıyor")

if __name__ == "__main__":
    print("🚀 Debug Test Başlıyor...\n")
    
    test_api()
    test_analysis()
    
    print("\n✅ Debug test tamamlandı!")