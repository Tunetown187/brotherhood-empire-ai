import asyncio
import logging
from web3 import Web3
from eth_account import Account
from flashbots import Flashbots
from typing import Dict, List
import json
from decimal import Decimal

class FlashbotsManager:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.setup_web3()
        self.setup_flashbots()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('FlashbotsManager')
        
    def load_config(self):
        """Load flashbots configuration"""
        try:
            with open('config/flashbots_config.json', 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            self.config = {}
            
    def setup_web3(self):
        """Setup Web3 connections"""
        self.w3 = Web3(Web3.HTTPProvider(self.config['eth_rpc']))
        self.account = Account.from_key(self.config['private_key'])
        
    def setup_flashbots(self):
        """Setup Flashbots connection"""
        self.flashbots = Flashbots(
            self.w3,
            self.account,
            self.config['flashbots_relay']
        )
        
    async def simulate_bundle(self, bundle: List[Dict]) -> Dict:
        """Simulate a flashbots bundle"""
        try:
            simulation = await self.flashbots.simulate(
                bundle,
                block_tag=self.w3.eth.block_number
            )
            
            return {
                'success': simulation.success,
                'gas_used': simulation.gas_used,
                'value': simulation.value,
                'profit': simulation.profit
            }
            
        except Exception as e:
            self.logger.error(f"Error simulating bundle: {str(e)}")
            return None
            
    async def send_bundle(self, bundle: List[Dict]) -> str:
        """Send a flashbots bundle"""
        try:
            # Simulate first
            simulation = await self.simulate_bundle(bundle)
            if not simulation['success']:
                return None
                
            # Calculate optimal gas price
            gas_price = await self.calculate_optimal_gas_price(simulation)
            
            # Send bundle
            tx_hash = await self.flashbots.send_bundle(
                bundle,
                target_block_number=self.w3.eth.block_number + 1,
                opts={
                    'gas_price': gas_price,
                    'gas_limit': int(simulation['gas_used'] * 1.1)
                }
            )
            
            return tx_hash
            
        except Exception as e:
            self.logger.error(f"Error sending bundle: {str(e)}")
            return None
            
    async def calculate_optimal_gas_price(self, simulation: Dict) -> int:
        """Calculate optimal gas price for profitability"""
        try:
            # Get current base fee
            base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']
            
            # Calculate minimum profitable gas price
            min_profit = Decimal(self.config['min_profit_eth'])
            gas_used = Decimal(simulation['gas_used'])
            
            max_gas_price = (Decimal(simulation['profit']) - min_profit) / gas_used
            
            # Add premium for higher success rate
            optimal_gas_price = int(max_gas_price * Decimal('1.1'))
            
            return max(optimal_gas_price, base_fee)
            
        except Exception as e:
            self.logger.error(f"Error calculating gas price: {str(e)}")
            return None
            
    async def create_arbitrage_bundle(
        self,
        token_address: str,
        amount: int,
        paths: List[List[str]]
    ) -> List[Dict]:
        """Create an arbitrage bundle"""
        try:
            bundle = []
            
            # Add token approval if needed
            if await self.needs_approval(token_address):
                bundle.append(
                    await self.create_approval_tx(token_address)
                )
                
            # Add swap transactions
            for path in paths:
                bundle.append(
                    await self.create_swap_tx(
                        path[0],
                        path[1],
                        amount,
                        path[2:]
                    )
                )
                
            return bundle
            
        except Exception as e:
            self.logger.error(f"Error creating bundle: {str(e)}")
            return None
            
    async def monitor_opportunities(self):
        """Monitor for arbitrage opportunities"""
        try:
            while True:
                # Get prices across exchanges
                prices = await self.get_prices()
                
                # Find profitable paths
                opportunities = await self.find_arbitrage_paths(prices)
                
                for opp in opportunities:
                    if opp['profit'] > self.config['min_profit_eth']:
                        # Create and send bundle
                        bundle = await self.create_arbitrage_bundle(
                            opp['token'],
                            opp['amount'],
                            opp['paths']
                        )
                        
                        if bundle:
                            await self.send_bundle(bundle)
                            
                await asyncio.sleep(1)  # Check every block
                
        except Exception as e:
            self.logger.error(f"Error monitoring opportunities: {str(e)}")
            await asyncio.sleep(60)
            
    async def find_arbitrage_paths(self, prices: Dict) -> List[Dict]:
        """Find profitable arbitrage paths"""
        opportunities = []
        
        # Check each token pair
        for token in prices:
            for dex1 in prices[token]:
                for dex2 in prices[token]:
                    if dex1 != dex2:
                        profit = self.calculate_profit(
                            prices[token][dex1],
                            prices[token][dex2]
                        )
                        
                        if profit > 0:
                            opportunities.append({
                                'token': token,
                                'profit': profit,
                                'paths': [
                                    [dex1, token],
                                    [token, dex2]
                                ]
                            })
                            
        return opportunities
        
    def calculate_profit(self, price1: Decimal, price2: Decimal) -> Decimal:
        """Calculate potential profit"""
        return abs(price1 - price2) / min(price1, price2)
        
    async def run_forever(self):
        """Run flashbots manager continuously"""
        try:
            while True:
                # Monitor for opportunities
                await self.monitor_opportunities()
                
                # Update gas price estimates
                await self.update_gas_estimates()
                
                # Clean up pending bundles
                await self.cleanup_pending()
                
                await asyncio.sleep(1)  # Update every block
                
        except Exception as e:
            self.logger.error(f"Error in flashbots manager: {str(e)}")
            await asyncio.sleep(60)
