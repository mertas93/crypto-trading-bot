#!/usr/bin/env python3
  """
  GitHub Actions üzerinde çalışan Crypto Trading Bot
  Mevcut trading_analyzer.py sisteminin aynısı - 40 dakikada bir tarama
  """

  import os
  import sys
  import json
  import requests
  import logging
  from datetime import datetime, timedelta
  import time
  from typing import Dict, List, Optional, Any
  import traceback
  import numpy as np

  # Logging ayarları
  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(levelname)s - %(message)s',
      handlers=[
          logging.FileHandler('crypto_bot.log'),
          logging.StreamHandler(sys.stdout)
      ]
  )
  logger = logging.getLogger(__name__)

  class CryptoBotGitHub:
      def __init__(self):
          """GitHub Actions ortamında çalışan bot - Aynı sistem"""
          # Telegram ayarları - Environment variables'dan al
          self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
          self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

          if not self.bot_token or not self.chat_id:
              raise ValueError("Telegram bot token ve chat ID environment variables olarak 
  ayarlanmalı!")

          # API ayarları - Orijinal sistem
          self.binance_api = "https://api.binance.com/api/v3/klines"
          self.binance_futures_api = "https://fapi.binance.com/fapi/v1"
          self.timeframes = ["1m", "3m", "5m", "30m"]

          # Headers - Bot detection bypass
          self.headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 
  (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
              'Accept': 'application/json',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en-US,en;q=0.9',
              'Connection': 'keep-alive',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'cross-site'
          }

          # Market data cache
          self.btc_data = None
          self.market_sentiment = None
          self.market_dominance = None

          # Trading positions - GitHub'dan yükle
          self.positions_data = []
          self.load_positions_from_file()

      def load_positions_from_file(self):
          """trading_positions.json dosyasını yükle"""
          try:
              with open('trading_positions.json', 'r', encoding='utf-8') as f:
                  data = json.load(f)
                  self.positions_data = data.get('positions', data)  # Backward 
  compatibility
                  logger.info(f"✅ {len(self.positions_data)} pozisyon yüklendi")
          except FileNotFoundError:
              logger.error("❌ trading_positions.json bulunamadı!")
              self.positions_data = []
          except Exception as e:
              logger.error(f"❌ Pozisyon dosyası yükleme hatası: {e}")
              self.positions_data = []

      def send_telegram_message(self, message: str) -> bool:
          """Telegram mesajı gönder"""
          try:
              url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
              data = {
                  'chat_id': self.chat_id,
                  'text': message,
                  'parse_mode': 'HTML',
                  'disable_web_page_preview': True
              }

              response = requests.post(url, data=data, timeout=10)
              response.raise_for_status()
              return True

          except Exception as e:
              logger.error(f"❌ Telegram mesaj gönderme hatası: {e}")
              return False

      def get_crypto_list(self) -> List[str]:
          """Binance'den USDT çiftlerini al - SADECE BİNANCE"""
          try:
              # Binance exchangeInfo - 24hr ticker ile kombinasyon
              logger.info("🔍 Binance'den coin listesi alınıyor...")

              # 1. Aktif trading çiftleri al - headers ile
              response = requests.get("https://api.binance.com/api/v3/exchangeInfo",
                                    headers=self.headers, timeout=30)
              response.raise_for_status()
              exchange_data = response.json()

              # Aktif USDT çiftleri filtrele
              active_usdt = []
              for symbol in exchange_data['symbols']:
                  if (symbol['symbol'].endswith('USDT') and
                      symbol['status'] == 'TRADING' and
                      symbol['symbol'] not in ['USDCUSDT', 'TUSDUSDT', 'FDUSDUSDT']):
                      active_usdt.append(symbol['symbol'])

              # 2. 24hr volume verisi al - sıralama için
              logger.info("📊 Volume verileri alınıyor...")
              response = requests.get("https://api.binance.com/api/v3/ticker/24hr",
                                    headers=self.headers, timeout=30)
              response.raise_for_status()
              volume_data = response.json()

              # Volume'a göre sırala
              volume_dict = {ticker['symbol']: float(ticker['quoteVolume']) for ticker in
  volume_data}

              # Sadece aktif USDT çiftlerini al ve volume'a göre sırala
              usdt_with_volume = []
              for symbol in active_usdt:
                  if symbol in volume_dict:
                      usdt_with_volume.append((symbol, volume_dict[symbol]))

              # Volume'a göre sırala (yüksekten düşüğe)
              usdt_with_volume.sort(key=lambda x: x[1], reverse=True)

              # İlk 500 coin - major coinleri öncelikle
              major_coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT',
  'SOLUSDT']
              other_coins = [coin[0] for coin in usdt_with_volume if coin[0] not in
  major_coins]

              final_list = major_coins + other_coins
              result = final_list[:500]

              logger.info(f"✅ Binance: {len(result)} USDT çifti alındı")
              return result

          except Exception as e:
              logger.error(f"❌ Binance API hatası: {e}")
              return []

  def main():
      """Ana fonksiyon"""
      try:
          logger.info("🤖 Crypto Trading Bot başlatılıyor...")

          # Bot'u başlat
          bot = CryptoBotGitHub()

          # Coin listesi test
          crypto_list = bot.get_crypto_list()
          if not crypto_list:
              bot.send_telegram_message("❌ Coin listesi alınamadı! Binance API sorunu")
              return 1

          # Basit durum raporu gönder
          report_msg = f"""🤖 <b>Crypto Bot Raporu</b>

  📊 <b>Durum:</b> Aktif
  🔍 <b>Coin listesi:</b> {len(crypto_list)} USDT çifti
  ⏰ <b>Zaman:</b> {datetime.now().strftime("%H:%M:%S")}

  🎯 <b>İlk 10 coin:</b>
  {', '.join(crypto_list[:10])}

  ✅ <b>Sistem hazır!</b> Gerçek tarama için tam kod aktifleştirilecek."""

          success = bot.send_telegram_message(report_msg)

          if success:
              logger.info("✅ Bot coin listesi başarıyla alındı")
          else:
              logger.error("❌ Telegram mesajı gönderilemedi")
              return 1

          return 0

      except Exception as e:
          logger.error(f"❌ Bot hatası: {str(e)}")
          return 1

  if __name__ == "__main__":
      sys.exit(main())
