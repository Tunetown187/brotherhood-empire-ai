import asyncio
import json
import base58
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.commitment_config import CommitmentLevel
from solders.message import MessageV0
from solders.hash import Hash
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solders.instruction import Instruction
from solders.rpc.config import RpcSendTransactionConfig
from solders.rpc.requests import SendVersionedTransaction
import requests
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PumpFunAgent:
    def __init__(self, private_key=None, min_sol=0.1, max_coins=3, slippage=10, priority_fee=0.005, sell_percentage=50, monitoring_interval=5):
        self.domain = "frontend-api.pump.fun"
        self.min_market_cap = 20000
        self.list_url = f"https://{self.domain}/coins/for-you?offset=0&limit=50&includeNsfw=false"
        self.monitor_url = f"https://{self.domain}/coins/"
        self.trade_url = "https://pumpportal.fun/api/trade-local"
        self.rpc_endpoint = "https://api.mainnet-beta.solana.com"
        self.client = Client(self.rpc_endpoint)
        
        # Trading parameters
        self.private_key = private_key
        self.keypair = Keypair.from_base58_string(private_key) if private_key else None
        self.public_key = str(self.keypair.pubkey()) if self.keypair else None
        self.min_sol = min_sol
        self.max_coins = max_coins
        self.slippage = slippage
        self.priority_fee = priority_fee
        self.sell_percentage = sell_percentage
        self.monitoring_interval = monitoring_interval
        
        # State tracking
        self.purchased_coins = {}  # {mint: {'initial_value': mcap, 'price_history': [], 'highest_seen': 0}}
        self.wallet_tokens = {}  # {mint: {'amount': amount, 'initial_value': value}}
        self.active_trades = {}
        
        # Smart selling parameters
        self.price_decline_trigger = 10  # Sell if price drops 10% from peak
        self.rapid_rise_trigger = 100  # Start monitoring for reversal after 100% gain
        self.profit_taking_levels = [200, 300, 400]  # Take profits at these percentage gains

    async def fetch_coin_data(self):
        """Fetch coin data from Pump.fun API"""
        try:
            response = requests.get(self.list_url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logging.error(f"Error fetching coin data: {e}")
            return None

    async def fetch_coin_by_mint(self, mint):
        """Fetch specific coin data by mint address"""
        try:
            response = requests.get(f"{self.monitor_url}{mint}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logging.error(f"Error fetching coin by mint: {e}")
            return None

    async def identify_low_cap_gems(self):
        """Identify potential low cap gems to trade"""
        coin_data = await self.fetch_coin_data()
        if not coin_data:
            return []
        
        potential_coins = []
        for coin in coin_data:
            if coin.get('usd_market_cap', 0) >= self.min_market_cap:
                potential_coins.append(coin)
                
        # Sort by market cap (ascending)
        potential_coins.sort(key=lambda x: x.get('usd_market_cap', float('inf')))
        return potential_coins[:self.max_coins]

    async def execute_trade(self, action, mint, amount, denominated_in_sol=False):
        """Execute a trade (buy/sell) on Pump.fun"""
        if not self.private_key:
            logging.error("No private key provided")
            return False
            
        try:
            keypair = Keypair.from_base58_string(self.private_key)
            public_key = str(keypair.pubkey())
            
            trade_data = {
                "action": action,
                "mint": mint,
                "amount": amount,
                "denominatedInSol": str(denominated_in_sol).lower(),
                "publicKey": public_key,
                "slippage": self.slippage,
                "priorityFee": self.priority_fee,
                "pool": "pump"
            }
            
            response = requests.post(self.trade_url, json=trade_data)
            if response.status_code != 200:
                logging.error(f"Trade failed: {response.text}")
                return False
                
            tx_bytes = base58.b58decode(response.json()['transaction'])
            tx = VersionedTransaction(VersionedTransaction.from_bytes(tx_bytes).message, [keypair])
            
            commitment = CommitmentLevel.Confirmed
            config = RpcSendTransactionConfig(preflight_commitment=commitment)
            send_req = SendVersionedTransaction(tx, config)
            
            response = requests.post(
                url=self.rpc_endpoint,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": send_req.method,
                    "params": send_req.to_json()
                }
            )
            
            if response.status_code == 200:
                logging.info(f"Trade executed successfully: {action} {mint}")
                return True
            
            logging.error(f"Transaction failed: {response.text}")
            return False
            
        except Exception as e:
            logging.error(f"Error executing trade: {e}")
            return False

    async def get_wallet_tokens(self):
        """Get all tokens in the wallet"""
        try:
            response = requests.get(
                url=self.rpc_endpoint,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getTokenAccountsByOwner",
                    "params": [
                        self.public_key,
                        {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
                        {"encoding": "jsonParsed"}
                    ]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                tokens = {}
                for account in data.get('result', {}).get('value', []):
                    info = account.get('account', {}).get('data', {}).get('parsed', {}).get('info', {})
                    mint = info.get('mint')
                    amount = int(info.get('tokenAmount', {}).get('amount', 0))
                    if amount > 0:
                        tokens[mint] = {'amount': amount}
                return tokens
            return {}
            
        except Exception as e:
            logging.error(f"Error getting wallet tokens: {e}")
            return {}

    async def update_wallet_monitoring(self):
        """Update the list of tokens being monitored from wallet"""
        wallet_tokens = await self.get_wallet_tokens()
        
        # Add new tokens to monitoring
        for mint in wallet_tokens:
            if mint not in self.wallet_tokens:
                coin_data = await self.fetch_coin_by_mint(mint)
                if coin_data:
                    current_mcap = coin_data.get('usd_market_cap', 0)
                    self.wallet_tokens[mint] = {
                        'amount': wallet_tokens[mint]['amount'],
                        'initial_value': current_mcap,
                        'price_history': [current_mcap],
                        'highest_seen': current_mcap,
                        'name': coin_data.get('name', 'Unknown')
                    }
        
        # Remove tokens no longer in wallet
        for mint in list(self.wallet_tokens.keys()):
            if mint not in wallet_tokens:
                del self.wallet_tokens[mint]

    async def analyze_price_action(self, coin_data, price_info):
        """Smart analysis of price action to determine sell decision"""
        current_mcap = coin_data.get('usd_market_cap', 0)
        initial_value = price_info['initial_value']
        highest_seen = price_info['highest_seen']
        price_history = price_info['price_history'][-10:]  # Last 10 price points
        
        percentage_change = ((current_mcap - initial_value) / initial_value) * 100
        
        # Update highest seen price
        if current_mcap > highest_seen:
            price_info['highest_seen'] = current_mcap
            highest_seen = current_mcap
        
        # Calculate decline from peak
        decline_from_peak = ((highest_seen - current_mcap) / highest_seen) * 100
        
        # Decision logic
        should_sell = False
        reason = None
        
        # 1. Protect profits if we've seen a significant rise
        if percentage_change > self.rapid_rise_trigger:
            if decline_from_peak >= self.price_decline_trigger:
                should_sell = True
                reason = f"Price dropped {decline_from_peak:.2f}% from peak after {percentage_change:.2f}% rise"
        
        # 2. Take profits at predetermined levels
        for level in self.profit_taking_levels:
            if percentage_change >= level:
                should_sell = True
                reason = f"Taking profits at {level}% gain"
                break
        
        # 3. Detect rapid price reversal
        if len(price_history) >= 3:
            recent_trend = [b - a for a, b in zip(price_history[-3:], price_history[-2:])]
            if all(x < 0 for x in recent_trend) and percentage_change > 50:
                should_sell = True
                reason = "Detected price reversal pattern"
        
        return should_sell, reason, percentage_change

    async def monitor_all_positions(self):
        """Monitor all positions including wallet tokens"""
        while True:
            try:
                # Update wallet tokens
                await self.update_wallet_monitoring()
                
                # Monitor all tokens (both purchased and in wallet)
                all_tokens = {**self.purchased_coins, **self.wallet_tokens}
                
                # Clear console for clean output
                print("\033[2J\033[H")  # Clear screen and move cursor to top
                print(f"Monitoring {len(all_tokens)} tokens...")
                print("-" * 50)
                
                for mint, token_info in all_tokens.items():
                    coin_data = await self.fetch_coin_by_mint(mint)
                    if coin_data:
                        current_mcap = coin_data.get('usd_market_cap', 0)
                        if current_mcap > 0:
                            # Update price history
                            token_info['price_history'] = token_info.get('price_history', []) + [current_mcap]
                            if len(token_info['price_history']) > 20:
                                token_info['price_history'] = token_info['price_history'][-20:]
                            
                            # Update highest seen price
                            if current_mcap > token_info.get('highest_seen', 0):
                                token_info['highest_seen'] = current_mcap
                            
                            initial_value = token_info['initial_value']
                            percentage_change = ((current_mcap - initial_value) / initial_value) * 100
                            
                            # Color code based on percentage change
                            color = "\033[92m" if percentage_change >= 0 else "\033[91m"  # Green for positive, Red for negative
                            
                            # Print token status
                            print(f"Token: {coin_data.get('name', 'Unknown')}")
                            print(f"Current Change: {color}{percentage_change:.2f}%\033[0m")
                            print(f"Highest Seen: {((token_info['highest_seen'] - initial_value) / initial_value * 100):.2f}%")
                            print("-" * 30)
                            
                            # Check for sell conditions if it's in purchased_coins
                            if mint in self.purchased_coins:
                                should_sell, reason, _ = await self.analyze_price_action(coin_data, token_info)
                                if should_sell:
                                    print(f"SELLING {coin_data.get('name', 'Unknown')} - Reason: {reason}")
                                    if await self.execute_trade("sell", mint, "all"):
                                        del self.purchased_coins[mint]
                                        print(f"Successfully sold {coin_data.get('name', 'Unknown')}")
                                    else:
                                        print(f"Failed to sell {coin_data.get('name', 'Unknown')}")
                
            except Exception as e:
                logging.error(f"Error in monitor_all_positions: {e}")
            
            await asyncio.sleep(self.monitoring_interval)

    async def execute_tasks(self):
        """Main task execution loop"""
        # Start monitoring thread for all positions
        monitor_task = asyncio.create_task(self.monitor_all_positions())
        
        while True:
            try:
                # Identify and buy new coins
                low_cap_gems = await self.identify_low_cap_gems()
                
                for coin in low_cap_gems:
                    if coin['mint'] not in self.purchased_coins and coin['mint'] not in self.wallet_tokens:
                        logging.info(f"Attempting to buy {coin.get('name', 'Unknown')}")
                        if await self.execute_trade("buy", coin['mint'], self.min_sol, True):
                            self.purchased_coins[coin['mint']] = {
                                'initial_value': coin['usd_market_cap'],
                                'price_history': [coin['usd_market_cap']],
                                'highest_seen': coin['usd_market_cap']
                            }
                            logging.info(f"Successfully bought {coin.get('name', 'Unknown')}")
                
            except Exception as e:
                logging.error(f"Error in execute_tasks: {e}")
            
            await asyncio.sleep(30)  # Wait before looking for new opportunities

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Pump.fun Trading Bot with Agency Swarm Integration")
    parser.add_argument("--private-key", required=True, help="Your wallet's private key")
    parser.add_argument("--min", type=float, default=0.1, help="Minimum SOL per trade")
    parser.add_argument("--max-coins", type=int, default=3, help="Maximum number of coins to buy")
    parser.add_argument("--slippage", type=float, default=10, help="Slippage percentage")
    parser.add_argument("--priority-fee", type=float, default=0.005, help="Priority fee in SOL")
    parser.add_argument("--sell-percentage", type=float, default=50, help="Percentage change to trigger sell")
    parser.add_argument("--monitoring-interval", type=int, default=5, help="Monitoring interval in seconds")
    
    args = parser.parse_args()
    
    agent = PumpFunAgent(
        private_key=args.private_key,
        min_sol=args.min,
        max_coins=args.max_coins,
        slippage=args.slippage,
        priority_fee=args.priority_fee,
        sell_percentage=args.sell_percentage,
        monitoring_interval=args.monitoring_interval
    )
    
    asyncio.run(agent.execute_tasks())

if __name__ == "__main__":
    main()
