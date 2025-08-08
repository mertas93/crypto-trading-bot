# 🤖 Crypto Trading Bot

GitHub Actions üzerinde çalışan otomatik kripto tarama botu. 40 dakikada bir 500+ coin'i tarar ve eşleşen sinyalleri Telegram'a gönderir.

## 🚀 Özellikler

- ✅ **40 dakikada bir otomatik tarama**
- 📊 **500+ coin analizi** (Binance USDT çiftleri)
- 🎯 **Pozisyon eşleştirme sistemi** (44 faktör analizi)
- 📱 **Telegram bildirim** (HTML formatında)
- 🔄 **GitHub Actions tabanlı** (sunucu gerektirmez)
- 🛡️ **Rate limiting** ve hata yönetimi
- 📈 **Market rejimi analizi** (BULL/BEAR/RANGE)

## 📋 Kurulum

### 1. Repository'yi Fork Edin
Bu repository'yi kendi GitHub hesabınıza fork edin.

### 2. Telegram Bot Oluşturun
1. Telegram'da @BotFather'a gidin
2. `/newbot` komutunu kullanarak yeni bot oluşturun
3. Bot token'ınızı kaydedin

### 3. Chat ID'nizi Öğrenin
1. Bot'unuza mesaj gönderin
2. `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` adresine gidin
3. `chat.id` değerini kaydedin

### 4. GitHub Secrets Ayarlayın
Repository Settings > Secrets and variables > Actions'a gidin ve şunları ekleyin:

- `TELEGRAM_BOT_TOKEN`: Telegram bot token'ınız
- `TELEGRAM_CHAT_ID`: Chat ID'niz

### 5. GitHub Actions'ı Etkinleştirin
- Repository'nizde Actions sekmesine gidin
- Workflow'u enable edin
- İlk çalışma için "Run workflow" butonuna basın

## 🔧 Yapılandırma

### Tarama Sıklığı
`.github/workflows/crypto-bot.yml` dosyasında cron ifadesini değiştirin:
```yaml
schedule:
  - cron: '*/40 * * * *'  # 40 dakikada bir
```

### Position Data
`trading_positions.json` dosyası bot'un eşleştirme yapacağı pozisyon verilerini içerir. Bu dosyayı kendi trading geçmişinizle güncelleyebilirsiniz.

## 📊 Bot Nasıl Çalışır?

1. **Coin Listesi**: Binance'den aktif USDT çiftlerini alır
2. **Teknik Analiz**: Her coin için 4 timeframe'de (1m, 3m, 5m, 30m) MA analizi
3. **Eşleştirme**: Mevcut pozisyon verileriyle 44 faktör karşılaştırması
4. **Filtreleme**: Minimum %75 eşleşme oranı gerekir
5. **Bildirim**: En iyi 5 sinyali Telegram'a gönderir

## 📱 Mesaj Formatı

```
🤖 Crypto Bot - 14:30

📊 Market: BULL_TREND
🔍 Tarama: 500 coin
🎯 Sinyal: 3 eşleşme

🟢 1. ETHUSDT
   📈 LONG (%89.2)
   🔗 ETH-BTC
   ⭐ EXCELLENT

🔴 2. XRPUSDT
   📉 SHORT (%82.1)
   🔗 XRP-ETH
   ⭐ VERY_GOOD
```

## ⚠️ Önemli Notlar

- Bu bot **eğitim amaçlıdır** ve yatırım tavsiyesi değildir
- GitHub Actions **2000 dakika/ay** ücretsiz limit vardır
- Bot çalışmazsa Logs sekmesinden hataları kontrol edin
- API rate limiting nedeniyle bazen gecikmeler olabilir

## 🔍 Log ve Monitoring

- GitHub Actions > Workflow runs'dan çalışma loglarını görüntüleyebilirsiniz
- Bot otomatik olarak `crypto_bot.log` dosyası oluşturur
- Hata durumunda Telegram'a bildirim gönderir

## 📈 Geliştirme

Bot kodunu geliştirmek için:
1. `trading_bot.py` dosyasını düzenleyin
2. Değişiklikleri commit edin
3. GitHub Actions otomatik olarak yeni versiyonu çalıştırır

## 🆘 Sorun Giderme

### Bot Çalışmıyor
- GitHub Secrets'ın doğru ayarlandığını kontrol edin
- Actions sekmesinde workflow'un etkin olduğunu kontrol edin

### Telegram Mesajı Gelmiyor
- Bot token ve chat ID'nin doğru olduğunu kontrol edin
- Bot'a en az bir kez mesaj gönderdiğinizden emin olun

### Sinyaller Çok Az
- `trading_positions.json` dosyasının güncel olduğunu kontrol edin
- Minimum eşleşme oranını düşürmek için kodu düzenleyin

## 📄 Lisans

Bu proje MIT lisansı altında yayınlanmıştır.

---

⭐ **Beğendiyseniz yıldız vermeyi unutmayın!**