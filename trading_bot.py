#!/usr/bin/env python3
"""
Ultra Basit Trading Bot - Takılma Sorunu Çözümü
"""
import requests
import time
from datetime import datetime

def send_telegram_message(message):
    """Telegram mesajı gönder"""
    try:
        bot_token = "8036527191:AAEGeUZHDb4AMLICFGmGl6OdrN4hrSaUpoQ"
        chat_id = "1119272011"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=5)
        if response.status_code == 200:
            print("✅ Telegram mesajı gönderildi")
            return True
        else:
            print(f"❌ Telegram hatası: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram hatası: {e}")
        return False

def get_price_data(symbol):
    """CoinGecko'dan fiyat verisi al"""
    try:
        coin_map = {
            'BTCUSDT': 'bitcoin',
            'ETHUSDT': 'ethereum', 
            'BNBUSDT': 'binancecoin'
        }
        
        if symbol not in coin_map:
            return None
            
        coin_id = coin_map[symbol]
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            coin_data = data.get(coin_id, {})
            
            price = coin_data.get('usd')
            change_24h = coin_data.get('usd_24h_change')
            
            if price and change_24h is not None:
                return {
                    'price': price,
                    'change_24h': change_24h
                }
                
        return None
        
    except Exception as e:
        print(f"❌ {symbol} fiyat hatası: {e}")
        return None

def analyze_simple():
    """Ultra basit analiz"""
    print("🚀 Ultra Basit Trading Analizi Başlıyor...")
    
    # Sadece 3 major coin
    coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
    signals = []
    
    for symbol in coins:
        print(f"⏳ {symbol} analiz ediliyor...")
        
        price_data = get_price_data(symbol)
        
        if price_data:
            price = price_data['price']
            change_24h = price_data['change_24h']
            
            print(f"   💰 Fiyat: ${price:,.2f}")
            print(f"   📊 24h Değişim: %{change_24h:.2f}")
            
            # Basit sinyal kuralı: %5+ hareket varsa sinyal
            if abs(change_24h) > 5:
                signal_type = "🟢 LONG" if change_24h > 0 else "🔴 SHORT"
                signals.append({
                    'symbol': symbol.replace('USDT', ''),
                    'price': price,
                    'change': change_24h,
                    'type': signal_type
                })
                print(f"   🎯 SİGNAL: {signal_type}")
            else:
                print(f"   ⚪ Sinyal yok")
        else:
            print(f"   ❌ Veri alınamadı")
        
        # 2 saniye bekle
        time.sleep(2)
    
    # Sinyal varsa Telegram gönder
    if signals:
        timestamp = datetime.now().strftime('%H:%M:%S')
        message = f"""🚀 <b>TRADING SİGNALLER</b>

⏰ <b>Zaman:</b> {timestamp}
🎯 <b>Sinyal Sayısı:</b> {len(signals)}

"""
        
        for signal in signals:
            message += f"""💰 <b>{signal['symbol']}</b>
   💲 Fiyat: ${signal['price']:,.2f}
   📈 Değişim: %{signal['change']:.2f}
   🎯 Sinyal: {signal['type']}

"""
        
        message += "🤖 <i>Basit trading analizi</i>"
        
        print(f"\n📱 {len(signals)} sinyal bulundu - Telegram gönderiliyor...")
        send_telegram_message(message)
        
    else:
        print(f"\n📭 Sinyal bulunamadı")
    
    print(f"\n✅ Analiz tamamlandı!")

if __name__ == "__main__":
    analyze_simple()