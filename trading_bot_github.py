#!/usr/bin/env python3
"""
GitHub Actions crypto trading bot
"""

import os
import sys
import json
import requests
import logging
from datetime import datetime
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CryptoBotGitHub:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.bot_token or not self.chat_id:
            raise ValueError("Telegram credentials required")
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def send_telegram_message(self, message: str) -> bool:
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Telegram error: {e}")
            return False

    def get_crypto_list(self) -> List[str]:
        try:
            logger.info("Getting coin list from Binance...")
            
            response = requests.get(
                "https://api.binance.com/api/v3/exchangeInfo", 
                headers=self.headers, 
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            usdt_pairs = []
            for symbol in data['symbols']:
                if (symbol['symbol'].endswith('USDT') and 
                    symbol['status'] == 'TRADING'):
                    usdt_pairs.append(symbol['symbol'])
            
            major_coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT']
            other_coins = [coin for coin in usdt_pairs if coin not in major_coins]
            result = major_coins + other_coins[:496]
            
            logger.info(f"Got {len(result)} coins")
            return result
            
        except Exception as e:
            logger.error(f"Binance API error: {e}")
            return []

def main():
    try:
        logger.info("Starting crypto bot...")
        
        bot = CryptoBotGitHub()
        
        crypto_list = bot.get_crypto_list()
        if not crypto_list:
            bot.send_telegram_message("❌ Could not get coin list!")
            return 1
        
        report = f"""🤖 <b>Crypto Bot Report</b>

📊 <b>Status:</b> Active
🔍 <b>Coins:</b> {len(crypto_list)} USDT pairs
⏰ <b>Time:</b> {datetime.now().strftime("%H:%M:%S")}

🎯 <b>Top 10:</b>
{', '.join(crypto_list[:10])}

✅ <b>System ready!</b>"""

        success = bot.send_telegram_message(report)
        
        if success:
            logger.info("Success!")
        else:
            logger.error("Failed!")
            return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())