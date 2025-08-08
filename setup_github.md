# 🔧 GitHub Setup Rehberi

## 1. GitHub Repository Oluşturma

1. GitHub'da yeni repository oluşturun:
   - Repository name: `crypto-trading-bot`
   - Public (veya Private)
   - Initialize with README ✗ (biz ekleyeceğiz)

## 2. Dosyaları Yükleme

Şu dosyaları repository'nize yükleyin:

```
crypto-trading-bot/
├── .github/
│   └── workflows/
│       └── crypto-bot.yml
├── trading_bot.py
├── trading_positions.json
├── requirements.txt
├── test_bot.py
├── README.md
└── setup_github.md
```

## 3. GitHub Secrets Ayarlama

Repository Settings > Secrets and variables > Actions > New repository secret:

### TELEGRAM_BOT_TOKEN
- Name: `TELEGRAM_BOT_TOKEN`
- Secret: `8036527191:AAEGeUZHDb4AMLICFGmGl6OdrN4hrSaUpoQ`

### TELEGRAM_CHAT_ID  
- Name: `TELEGRAM_CHAT_ID`
- Secret: `1119272011`

## 4. GitHub Actions Etkinleştirme

1. Repository'de **Actions** sekmesine gidin
2. "I understand my workflows..." butonuna tıklayın
3. İlk workflow'u manuel çalıştırmak için **Run workflow** butonuna basın

## 5. İlk Test

1. Actions > Crypto Trading Bot > Run workflow
2. Workflow tamamlandığında Telegram'ı kontrol edin
3. Başarılı mesaj gelirse bot çalışıyor demektir

## 6. Cron Schedule Açıklaması

```yaml
schedule:
  - cron: '*/40 * * * *'
```

- `*/40`: Her 40 dakikada bir
- `*`: Her saat
- `*`: Her gün  
- `*`: Her ay
- `*`: Haftanın her günü

### Alternatif Zamanlamalar:

```yaml
# Her 30 dakikada bir
- cron: '*/30 * * * *'

# Her 1 saatte bir
- cron: '0 * * * *'  

# Her 2 saatte bir
- cron: '0 */2 * * *'

# Sadece iş saatleri (09:00-17:00)
- cron: '*/40 9-17 * * 1-5'
```

## 7. Troubleshooting

### Bot Çalışmıyor
- [ ] Secrets doğru ayarlandı mı?
- [ ] Actions etkin mi?
- [ ] trading_positions.json var mı?

### Telegram Mesajı Gelmiyor  
- [ ] Bot token doğru mu?
- [ ] Chat ID doğru mu?
- [ ] Bot'a en az 1 mesaj gönderildi mi?

### Çok Az Sinyal
- [ ] trading_positions.json dosyası güncel mi?
- [ ] Minimum eşleşme %75 - çok yüksek olabilir

## 8. GitHub Actions Limits

- **Free**: 2000 dakika/ay
- **Pro**: 3000 dakika/ay  
- **Team**: 10000 dakika/ay

### Maliyet Hesaplama
- 40dk'da bir = 36 çalışma/gün
- Her çalışma ~3-5 dakika
- Günlük: 36 × 4 = 144 dakika
- Aylık: 144 × 30 = 4320 dakika ❌

**Öneriler:**
- 1 saatte bir: 24 × 4 = 96 dakika/gün = ~2880 dakika/ay ✅
- Sadece iş saatleri: 9 × 4 = 36 dakika/gün = ~1080 dakika/ay ✅

## 9. İleri Düzey Ayarlar

### Sadece Major Coinler
`trading_bot.py` dosyasında:
```python
# İlk 50 coin yerine major coinler
major_coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT']
return major_coins + [coin for coin in usdt_pairs if coin not in major_coins][:50]
```

### Minimum Eşleşme Oranı
```python
if score > best_score and score >= 65:  # %75 yerine %65
```

### Daha Fazla Sinyal
```python
top_matches = sorted(matches, key=lambda x: x['match_percentage'], reverse=True)[:10]  # 5 yerine 10
```

## 10. Repository Yapısı Kontrolü

Yükleme öncesi kontrol listesi:
- [ ] `.github/workflows/crypto-bot.yml` ✅
- [ ] `trading_bot.py` ✅  
- [ ] `trading_positions.json` ✅
- [ ] `requirements.txt` ✅
- [ ] `README.md` ✅
- [ ] GitHub Secrets ayarlandı ✅
- [ ] Actions etkin ✅

**🎉 Hazırsınız! Repository'yi oluşturup dosyaları yükleyin.**