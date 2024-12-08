import ccxt
import pandas as pd
import numpy as np
from typing import Dict, List
import json
from pathlib import Path
import asyncio
import logging
from datetime import datetime
from cryptography.fernet import Fernet
from web3 import Web3
import ta
from dotenv import load_dotenv
import os

class CryptoManager:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.setup_encryption()
        self.setup_exchanges()
        self.setup_wallets()
        
    def setup_logging(self):
        """Setup logging for the crypto manager"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('crypto_manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('CryptoManager')
        
    def load_config(self):
        """Load configuration and API keys"""
        load_dotenv()
        self.config = {
            'binance_api_key': os.getenv('BINANCE_API_KEY'),
            'binance_secret': os.getenv('BINANCE_SECRET'),
            'coinbase_api_key': os.getenv('COINBASE_API_KEY'),
            'coinbase_secret': os.getenv('COINBASE_SECRET'),
            'infura_key': os.getenv('INFURA_KEY')
        }
        
    def setup_encryption(self):
        """Setup encryption for sensitive data"""
        key_file = Path('crypto_key.key')
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)
        
    def setup_exchanges(self):
        """Setup cryptocurrency exchange connections"""
        self.exchanges = {}
        
        # Setup Binance
        if self.config['binance_api_key'] and self.config['binance_secret']:
            self.exchanges['binance'] = ccxt.binance({
                'apiKey': self.config['binance_api_key'],
                'secret': self.config['binance_secret'],
                'enableRateLimit': True
            })
            
        # Setup Coinbase Pro
        if self.config['coinbase_api_key'] and self.config['coinbase_secret']:
            self.exchanges['coinbase'] = ccxt.coinbasepro({
                'apiKey': self.config['coinbase_api_key'],
                'secret': self.config['coinbase_secret'],
                'enableRateLimit': True
            })
            
    def setup_wallets(self):
        """Setup Web3 connection and wallet management"""
        if self.config['infura_key']:
            self.w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{self.config['infura_key']}"))
        self.wallets = self.load_wallets()
        
    def load_wallets(self) -> Dict:
        """Load encrypted wallet information"""
        wallet_file = Path('wallets.json')
        if wallet_file.exists():
            with open(wallet_file, 'r') as f:
                encrypted_data = f.read()
                decrypted_data = self.cipher.decrypt(encrypted_data.encode())
                return json.loads(decrypted_data)
        return {}
        
    def save_wallets(self):
        """Save encrypted wallet information"""
        encrypted_data = self.cipher.encrypt(json.dumps(self.wallets).encode())
        with open('wallets.json', 'w') as f:
            f.write(encrypted_data.decode())
            
    async def get_market_data(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> pd.DataFrame:
        """Get market data with technical indicators"""
        try:
            # Get OHLCV data from Binance
            ohlcv = self.exchanges['binance'].fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Add technical indicators
            df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
            df['macd'] = ta.trend.MACD(df['close']).macd()
            df['bb_high'] = ta.volatility.BollingerBands(df['close']).bollinger_hband()
            df['bb_low'] = ta.volatility.BollingerBands(df['close']).bollinger_lband()
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error getting market data: {str(e)}")
            return None
            
    async def analyze_market(self, symbol: str) -> Dict:
        """Analyze market conditions"""
        df = await self.get_market_data(symbol)
        if df is None:
            return None
            
        analysis = {
            'symbol': symbol,
            'current_price': df['close'].iloc[-1],
            'rsi': df['rsi'].iloc[-1],
            'macd': df['macd'].iloc[-1],
            'is_oversold': df['rsi'].iloc[-1] < 30,
            'is_overbought': df['rsi'].iloc[-1] > 70,
            'trend': 'bullish' if df['macd'].iloc[-1] > 0 else 'bearish',
            'volatility': df['close'].std() / df['close'].mean()
        }
        
        return analysis
        
    async def place_order(self, exchange: str, symbol: str, side: str, amount: float, price: float = None):
        """Place a new order on specified exchange"""
        try:
            if exchange not in self.exchanges:
                raise ValueError(f"Exchange {exchange} not configured")
                
            # Place market or limit order
            if price:
                order = self.exchanges[exchange].create_limit_order(
                    symbol=symbol,
                    side=side,
                    amount=amount,
                    price=price
                )
            else:
                order = self.exchanges[exchange].create_market_order(
                    symbol=symbol,
                    side=side,
                    amount=amount
                )
                
            self.logger.info(f"Order placed: {order}")
            return order
            
        except Exception as e:
            self.logger.error(f"Error placing order: {str(e)}")
            return None
            
    async def get_portfolio_value(self) -> Dict:
        """Get total portfolio value across all exchanges"""
        total_value = 0
        portfolio = {}
        
        for exchange_id, exchange in self.exchanges.items():
            try:
                balance = exchange.fetch_balance()
                for currency, amount in balance['total'].items():
                    if amount > 0:
                        # Get current price in USD
                        try:
                            ticker = exchange.fetch_ticker(f"{currency}/USDT")
                            usd_value = amount * ticker['last']
                            total_value += usd_value
                            portfolio[currency] = {
                                'amount': amount,
                                'usd_value': usd_value
                            }
                        except:
                            continue
                            
            except Exception as e:
                self.logger.error(f"Error getting {exchange_id} balance: {str(e)}")
                
        return {
            'total_value_usd': total_value,
            'holdings': portfolio
        }
        
    def add_wallet(self, name: str, address: str, private_key: str = None):
        """Add a new wallet (encrypted)"""
        if private_key:
            private_key = self.cipher.encrypt(private_key.encode()).decode()
        
        self.wallets[name] = {
            'address': address,
            'private_key': private_key
        }
        self.save_wallets()
        
    async def monitor_wallets(self):
        """Monitor wallet balances and transactions"""
        while True:
            for name, wallet in self.wallets.items():
                try:
                    balance = self.w3.eth.get_balance(wallet['address'])
                    eth_balance = self.w3.from_wei(balance, 'ether')
                    self.logger.info(f"Wallet {name} balance: {eth_balance} ETH")
                except Exception as e:
                    self.logger.error(f"Error monitoring wallet {name}: {str(e)}")
            
            await asyncio.sleep(300)  # Check every 5 minutes
            
    async def run_forever(self):
        """Run the crypto manager continuously"""
        while True:
            try:
                # Monitor portfolio value
                portfolio = await self.get_portfolio_value()
                self.logger.info(f"Current portfolio value: ${portfolio['total_value_usd']:.2f}")
                
                # Analyze major markets
                for symbol in ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']:
                    analysis = await self.analyze_market(symbol)
                    if analysis:
                        self.logger.info(f"Market analysis for {symbol}: {analysis}")
                
                await asyncio.sleep(60)  # Update every minute
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying
                
if __name__ == "__main__":
    manager = CryptoManager()
    asyncio.run(manager.run_forever())
