#!/usr/bin/env python3
"""
Market Bilgisi Görüntüleyici - Sadece market durumu
"""
import requests
import json
import os
from datetime import datetime
import time

class MarketInfo:
    def __init__(self):
        self.binance_api = "https://api.binance.com/api/v3"
        
        # Telegram ayarları
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', "8036527191:AAEGeUZHDb4AMLICFGmGl6OdrN4hrSaUpoQ")
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', "1119272011")

    def send_telegram_message(self, message):
        """Telegram mesajı gönder"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                print("✅ Telegram mesajı gönderildi")
                return True
            else:
                print(f"❌ Telegram hatası: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Telegram hatası: {e}")
            return False
        
    def get_btc_trend_consistency(self):
        """BTC trend tutarlılığını hesapla - TAM ORİJİNAL algoritma"""
        try:
            # Son 30 dakika 1m verisi çek (orijinal gibi)
            minutes = 30
            url = f"{self.binance_api}/klines"
            params = {
                'symbol': 'BTCUSDT',
                'interval': '1m',
                'limit': minutes
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                return 50
                
            klines = response.json()
            if not klines or len(klines) < minutes:
                return 50
            
            # Her dakika için trend yönünü belirle (orijinal algoritma)
            trends = []
            for i in range(len(klines) - 7):
                recent_closes = [float(klines[j][4]) for j in range(i, i + 7)]
                ma_7 = sum(recent_closes) / 7
                current_close = float(klines[i + 6][4])
                
                if current_close > ma_7:
                    trends.append('BULL')
                else:
                    trends.append('BEAR')
            
            if not trends:
                return 50
            
            bull_count = trends.count('BULL')
            bear_count = trends.count('BEAR')
            total_count = len(trends)
            
            # En baskın trendin oranı (orijinal gibi)
            trend_ratio = max(bull_count, bear_count) / total_count
            
            return round(trend_ratio * 100, 0)
            
        except:
            return 50

    def calculate_ma(self, prices, period):
        """Moving Average hesapla"""
        try:
            if len(prices) < period:
                return None
            return sum(prices[-period:]) / period
        except:
            return None

    def get_market_regime(self):
        """Market rejimini belirle - orijinal algoritma"""
        try:
            # BTC 15m verisi çek (orijinal gibi)
            url = f"{self.binance_api}/klines"
            params = {
                'symbol': 'BTCUSDT',
                'interval': '15m',
                'limit': 100
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                closes = [float(k[4]) for k in data]
                
                # MA'ları hesapla (orijinal algoritma)
                ma_7 = self.calculate_ma(closes, 7)
                ma_25 = self.calculate_ma(closes, 25) 
                ma_99 = self.calculate_ma(closes, 99)
                
                if None in [ma_7, ma_25, ma_99]:
                    return "BEAR TREND (BTC MA99>MA25>MA7 - Düşüş trendi)"
                
                # MA sıralaması belirle (orijinal gibi)
                if ma_7 > ma_25 > ma_99:
                    return "BULL TREND (BTC MA7>MA25>MA99 - Yükseliş trendi)"
                elif ma_99 > ma_25 > ma_7:
                    return "BEAR TREND (BTC MA99>MA25>MA7 - Düşüş trendi)"
                else:
                    return "RANGE MARKET (BTC yatay hareket - Trend belirsiz)"
            
            return "BEAR TREND (BTC MA99>MA25>MA7 - Düşüş trendi)"
        except:
            return "BEAR TREND (BTC MA99>MA25>MA7 - Düşüş trendi)"

    def get_multi_tf_info(self):
        """Multi-TF bilgisi - orijinal algoritma"""
        try:
            # Orijinal timeframe'ler: 5m, 30m, 1h
            timeframes = ['5m', '30m', '1h']
            bull_confirmations = 0
            
            for tf in timeframes:
                url = f"{self.binance_api}/klines"
                params = {
                    'symbol': 'BTCUSDT',
                    'interval': tf,
                    'limit': 100
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if len(data) < 99:
                        continue
                        
                    closes = [float(k[4]) for k in data]
                    
                    # MA'ları hesapla
                    ma_7 = self.calculate_ma(closes, 7)
                    ma_25 = self.calculate_ma(closes, 25)
                    ma_99 = self.calculate_ma(closes, 99)
                    
                    if None in [ma_7, ma_25, ma_99]:
                        continue
                    
                    # BULLISH trend kontrol (TAM ORİJİNAL)
                    current_price = closes[-1]
                    if ma_7 > ma_25 > ma_99 and current_price > ma_7:
                        bull_confirmations += 1
            
            # Orijinal formata uygun sonuç
            if bull_confirmations == 3:
                return f"{bull_confirmations}/3 (Mükemmel)"
            elif bull_confirmations >= 2:
                return f"{bull_confirmations}/3 (İyi)"
            else:
                return f"{bull_confirmations}/3 (Riskli)"
            
        except:
            return "0/3 (Riskli)"

    def calculate_rsi(self, prices, period=14):
        """RSI hesaplama"""
        try:
            if len(prices) < period + 1:
                return 50
                
            deltas = []
            for i in range(1, len(prices)):
                deltas.append(prices[i] - prices[i-1])
            
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]
            
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            
            if avg_loss == 0:
                return 100
                
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
            
        except:
            return 50

    def display_info(self):
        """Market bilgilerini göster ve Telegram'a gönder"""
        # Market rejimi
        regime = self.get_market_regime()
        print(f"MARKET REJIMİ: ✅ Rejim: {regime}")
        
        # Diğer bilgiler
        print("DİĞER BİLGİLER:")
        
        # BTC Trend tutarlılığı
        btc_consistency = self.get_btc_trend_consistency()
        
        # Tutarlılık durumuna göre emoji belirle
        if btc_consistency >= 75:
            btc_emoji = "✅"
            btc_status = "İyi"
        else:
            btc_emoji = "⚠️"
            btc_status = "Karışık"
        
        print(f"{btc_emoji} BTC Trend Tutarlılığı: {btc_consistency}% ({btc_status})")
        
        # Multi-TF
        multi_tf_result = self.get_multi_tf_info()
        
        # Multi-TF durumuna göre emoji belirle
        if "Mükemmel" in multi_tf_result:
            multi_emoji = "✅"
        elif "İyi" in multi_tf_result:
            multi_emoji = "⚠️"
        else:
            multi_emoji = "❌"
            
        print(f"{multi_emoji} Multi-TF (30dk odak): {multi_tf_result}")
        
        # Telegram mesajı oluştur
        telegram_message = f"""<b>📊 MARKET DURUMU</b>

<b>MARKET REJIMİ:</b> ✅ Rejim: {regime}

<b>DİĞER BİLGİLER:</b>
{btc_emoji} <b>BTC Trend Tutarlılığı:</b> {btc_consistency}% ({btc_status})
{multi_emoji} <b>Multi-TF (30dk odak):</b> {multi_tf_result}

⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🤖 <i>Otomatik market analizi</i>"""
        
        # Telegram'a gönder
        self.send_telegram_message(telegram_message)

if __name__ == "__main__":
    market = MarketInfo()
    market.display_info()