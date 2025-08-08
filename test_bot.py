#!/usr/bin/env python3
"""
Bot'u yerel olarak test etmek için
"""

import os
import sys
import logging

# Test için environment variables
os.environ['TELEGRAM_BOT_TOKEN'] = '8036527191:AAEGeUZHDb4AMLICFGmGl6OdrN4hrSaUpoQ'
os.environ['TELEGRAM_CHAT_ID'] = '1119272011'

# Trading bot'u import et
from trading_bot import CryptoBotGitHub

def test_basic_functionality():
    """Temel fonksiyonları test et"""
    print("🔍 Bot temel testleri...")
    
    try:
        bot = CryptoBotGitHub()
        print(f"✅ Bot başlatıldı - {len(bot.positions_data)} pozisyon yüklendi")
        
        # Market rejimi test
        regime = bot.get_current_market_regime()
        print(f"📊 Market rejimi: {regime}")
        
        # Coin listesi test (sadece ilk 10)
        coins = bot.get_crypto_list()[:10]
        print(f"🪙 Test için {len(coins)} coin: {coins}")
        
        # Tek coin analizi test
        if coins:
            test_coin = coins[0]
            print(f"🔍 {test_coin} analiz ediliyor...")
            
            analysis = bot.scan_single_coin(test_coin)
            if analysis:
                print(f"✅ Analiz başarılı: {analysis}")
                
                # Eşleşme testi
                match = bot.find_matches(test_coin, analysis)
                if match:
                    print(f"🎯 Eşleşme bulundu: {match}")
                else:
                    print("⚪ Eşleşme bulunamadı")
            else:
                print("❌ Analiz başarısız")
        
        print("\n✅ Temel testler tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return False

def test_telegram_message():
    """Telegram mesaj gönderme test"""
    print("\n📱 Telegram mesaj testi...")
    
    try:
        bot = CryptoBotGitHub()
        
        test_message = """🤖 <b>Test Mesajı</b>

📊 <b>Market:</b> TEST_MODE
🔍 <b>Tarama:</b> Test
🎯 <b>Sonuç:</b> Bot çalışıyor!

⚠️ <i>Bu bir test mesajıdır.</i>"""
        
        success = bot.send_telegram_message(test_message)
        
        if success:
            print("✅ Telegram mesajı başarıyla gönderildi!")
            return True
        else:
            print("❌ Telegram mesajı gönderilemedi!")
            return False
            
    except Exception as e:
        print(f"❌ Telegram test hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🚀 Crypto Bot Test Süreci Başlıyor...\n")
    
    # Temel testler
    basic_ok = test_basic_functionality()
    
    # Telegram testi
    telegram_ok = test_telegram_message()
    
    print(f"\n📋 Test Sonuçları:")
    print(f"   ✅ Temel fonksiyonlar: {'✓' if basic_ok else '✗'}")
    print(f"   📱 Telegram mesajlaşma: {'✓' if telegram_ok else '✗'}")
    
    if basic_ok and telegram_ok:
        print("\n🎉 Tüm testler başarılı! Bot GitHub'a yüklenmeye hazır.")
        return 0
    else:
        print("\n⚠️ Bazı testler başarısız. Lütfen hataları kontrol edin.")
        return 1

if __name__ == "__main__":
    sys.exit(main())