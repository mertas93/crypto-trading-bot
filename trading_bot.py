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
            # CryptoCompare API - 30 dakika 1m verisi
            minutes = 30
            url = f"https://min-api.cryptocompare.com/data/v2/histominute"
            params = {
                'fsym': 'BTC',
                'tsym': 'USDT', 
                'limit': minutes
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                return 50
                
            data = response.json()
            if 'Data' not in data or 'Data' not in data['Data']:
                return 50
                
            klines = data['Data']['Data']
            if not klines or len(klines) < minutes:
                return 50
            
            # Her dakika için trend yönünü belirle (CryptoCompare format)
            trends = []
            for i in range(len(klines) - 7):
                recent_closes = [float(klines[j]['close']) for j in range(i, i + 7)]
                ma_7 = sum(recent_closes) / 7
                current_close = float(klines[i + 6]['close'])
                
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
            # CryptoCompare API - 15m verisi
            url = f"https://min-api.cryptocompare.com/data/v2/histominute"
            params = {
                'fsym': 'BTC',
                'tsym': 'USDT',
                'limit': 100,
                'aggregate': 15
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'Data' not in data or 'Data' not in data['Data']:
                    return "BEAR TREND (BTC MA99>MA25>MA7 - Düşüş trendi)"
                    
                candles = data['Data']['Data']
                closes = [float(candle['close']) for candle in candles]
                
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
        """Multi-TF bilgisi - BULL ve BEAR analizi"""
        try:
            # Timeframe'ler: 5m, 30m, 1h
            timeframes = ['5m', '30m', '1h']
            bull_confirmations = 0
            bear_confirmations = 0
            
            for tf in timeframes:
                try:
                    # CryptoCompare API - coğrafi kısıt yok
                    limit_map = {'5m': 100, '30m': 100, '1h': 100}
                    url = f"https://min-api.cryptocompare.com/data/v2/histominute"
                    
                    if tf == '5m':
                        params = {'fsym': 'BTC', 'tsym': 'USDT', 'limit': 500, 'aggregate': 5}
                    elif tf == '30m':
                        params = {'fsym': 'BTC', 'tsym': 'USDT', 'limit': 100, 'aggregate': 30}
                    elif tf == '1h':
                        url = f"https://min-api.cryptocompare.com/data/v2/histohour"
                        params = {'fsym': 'BTC', 'tsym': 'USDT', 'limit': 100}
                    
                    response = requests.get(url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # CryptoCompare response format
                        if 'Data' not in data or 'Data' not in data['Data']:
                            print(f"⚠️ {tf}: CryptoCompare veri formatı hatası")
                            continue
                            
                        candles = data['Data']['Data']
                        if len(candles) < 99:
                            print(f"⚠️ {tf}: Yetersiz veri ({len(candles)} < 99)")
                            continue
                            
                        # CryptoCompare'de close price 'close' alanında
                        closes = [float(candle['close']) for candle in candles]
                        
                        # MA'ları hesapla
                        ma_7 = self.calculate_ma(closes, 7)
                        ma_25 = self.calculate_ma(closes, 25)
                        ma_99 = self.calculate_ma(closes, 99)
                        
                        if None in [ma_7, ma_25, ma_99]:
                            print(f"⚠️ {tf}: MA hesaplama hatası")
                            continue
                        
                        current_price = closes[-1]
                        
                        # BULLISH trend kontrol
                        if ma_7 > ma_25 > ma_99 and current_price > ma_7:
                            bull_confirmations += 1
                            print(f"✅ {tf}: BULL confirmation")
                        # BEARISH trend kontrol
                        elif ma_99 > ma_25 > ma_7 and current_price < ma_7:
                            bear_confirmations += 1
                            print(f"✅ {tf}: BEAR confirmation")
                        else:
                            print(f"➖ {tf}: Range market")
                    else:
                        print(f"❌ {tf}: API hatası ({response.status_code})")
                    
                    time.sleep(0.5)  # Rate limit önlemi
                    
                except Exception as e:
                    print(f"❌ {tf}: {str(e)[:50]}")
                    continue
            
            # Sonuç formatla
            if bull_confirmations == 3:
                return {"type": "BULL", "count": f"{bull_confirmations}/3", "status": "Mükemmel", "bear_count": bear_confirmations}
            elif bear_confirmations == 3:
                return {"type": "BEAR", "count": f"{bear_confirmations}/3", "status": "Mükemmel", "bull_count": bull_confirmations}
            elif bull_confirmations >= 2:
                return {"type": "BULL", "count": f"{bull_confirmations}/3", "status": "İyi", "bear_count": bear_confirmations}
            elif bear_confirmations >= 2:
                return {"type": "BEAR", "count": f"{bear_confirmations}/3", "status": "İyi", "bull_count": bull_confirmations}
            else:
                return {"type": "MIX", "count": f"{bull_confirmations}B-{bear_confirmations}Be/3", "status": "Karışık", "bull_count": bull_confirmations, "bear_count": bear_confirmations}
            
        except:
            return {"type": "ERROR", "count": "0/3", "status": "Veri Yok", "bull_count": 0, "bear_count": 0}

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
        if multi_tf_result["status"] == "Mükemmel":
            if multi_tf_result["type"] == "BULL":
                multi_emoji = "🚀"
            else:  # BEAR
                multi_emoji = "🐻"
        elif multi_tf_result["status"] == "İyi":
            multi_emoji = "⚠️"
        else:
            multi_emoji = "❌"
            
        print(f"{multi_emoji} Multi-TF (30dk odak): {multi_tf_result['count']} ({multi_tf_result['status']} - {multi_tf_result['type']})")
        
        # Market Rejimi trend tespiti
        regime_type = "BULL" if "BULL" in regime else "BEAR" if "BEAR" in regime else "RANGE"
        
        # TELEGRAM MESAJI GÖNDERME LOGİĞİ
        send_message = False
        message_type = ""
        
        if multi_tf_result["type"] in ["BULL", "BEAR"] and multi_tf_result["status"] == "Mükemmel" and btc_consistency >= 75:
            # GÜÇLÜ SİNYAL KONTROLÜ - SADECE UYUMLU DURUMLAR
            if regime_type == multi_tf_result["type"]:
                # Market rejimi ve Multi-TF uyumlu
                send_message = True
                message_type = f"GÜÇLÜ {multi_tf_result['type']} SİNYALİ"
                message_icon = "🚀" if multi_tf_result['type'] == "BULL" else "🐻"
                message_title = f"{message_icon} <b>{message_type}!</b>"
            # ÇELİŞKİ DURUMU - MESAJ GÖNDERMEYİZ
        
        if send_message:
            # Telegram mesajı oluştur - SADECE UYUMLU SİNYALLER
            telegram_message = f"""{message_title}

<b>MARKET REJIMİ:</b> ✅ Rejim: {regime}

<b>DİĞER BİLGİLER:</b>
{btc_emoji} <b>BTC Trend Tutarlılığı:</b> {btc_consistency}% ({btc_status})
{multi_emoji} <b>Multi-TF (30dk odak):</b> {multi_tf_result['count']} ({multi_tf_result['status']} - {multi_tf_result['type']})

⏰ <b>Zaman:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 <b>ŞARTLAR SAĞLANDI:</b>
✅ Multi-TF: {multi_tf_result['count']} {multi_tf_result['status']}
✅ BTC Tutarlılık: {btc_consistency}% (≥75%)
✅ Market Uyumu: {regime_type} = {multi_tf_result['type']}

🤖 <i>Güçlü {multi_tf_result['type'].lower()} market sinyali tespit edildi!</i>"""
            
            # Telegram'a gönder
            print(f"\n{message_icon} {message_type} - Telegram mesajı gönderiliyor...")
            self.send_telegram_message(telegram_message)
        else:
            print(f"\n⏸️ Telegram mesajı gönderilmedi:")
            print(f"   Multi-TF: {multi_tf_result['count']} {multi_tf_result['status']} (gerekli: 3/3 Mükemmel)")
            print(f"   BTC Tutarlılık: {btc_consistency}% (gerekli: ≥75%)")
            if multi_tf_result["type"] in ["BULL", "BEAR"]:
                uyum_status = '✅ Uyumlu' if regime_type == multi_tf_result['type'] else '❌ Çelişki (mesaj gönderilmez)'
                print(f"   Market Uyumu: {regime_type} vs {multi_tf_result['type']} ({uyum_status})")

if __name__ == "__main__":
    market = MarketInfo()
    market.display_info()