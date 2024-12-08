import asyncio
import logging
from web3 import Web3
import json
from typing import Dict, List
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from technical_analysis import TechnicalAnalyzer
from risk_manager import RiskManager

class TradingManager:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.setup_components()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('TradingManager')
        
    def load_config(self):
        """Load trading configuration"""
        try:
            with open('config/trading_config.json', 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            self.config = {}
            
    def setup_components(self):
        """Setup trading components"""
        self.technical_analyzer = TechnicalAnalyzer()
        self.risk_manager = RiskManager()
        self.setup_web3()
        
    def setup_web3(self):
        """Setup Web3 connections"""
        self.w3 = {
            'eth': Web3(Web3.HTTPProvider(self.config['eth_rpc'])),
            'bsc': Web3(Web3.HTTPProvider(self.config['bsc_rpc'])),
            'polygon': Web3(Web3.HTTPProvider(self.config['polygon_rpc']))
        }
        
    async def analyze_token(self, token_address: str, chain: str) -> Dict:
        """Analyze token for trading"""
        try:
            # Get token info
            token_info = await self.get_token_info(token_address, chain)
            
            # Check for red flags
            security_check = await self.check_token_security(token_address, chain)
            
            # Analyze liquidity
            liquidity = await self.analyze_liquidity(token_address, chain)
            
            # Get technical indicators
            technicals = await self.technical_analyzer.get_indicators(token_address)
            
            return {
                'token': token_info,
                'security': security_check,
                'liquidity': liquidity,
                'technicals': technicals,
                'recommendation': self.generate_recommendation(
                    security_check,
                    liquidity,
                    technicals
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing token: {str(e)}")
            return None
            
    async def check_token_security(self, token_address: str, chain: str) -> Dict:
        """Check token security"""
        red_flags = []
        
        # Check contract verification
        if not await self.is_contract_verified(token_address, chain):
            red_flags.append("Contract not verified")
            
        # Check ownership
        if await self.is_ownership_concentrated(token_address):
            red_flags.append("Concentrated ownership")
            
        # Check for honeypot
        if await self.is_honeypot(token_address):
            red_flags.append("Potential honeypot")
            
        # Check for mint function
        if await self.has_mint_function(token_address):
            red_flags.append("Mint function present")
            
        return {
            'red_flags': red_flags,
            'risk_level': self.calculate_risk_level(red_flags)
        }
        
    async def analyze_liquidity(self, token_address: str, chain: str) -> Dict:
        """Analyze token liquidity"""
        try:
            # Get liquidity pools
            pools = await self.get_liquidity_pools(token_address)
            
            total_liquidity = sum(pool['liquidity'] for pool in pools)
            
            # Check if liquidity is locked
            locked_liquidity = await self.check_locked_liquidity(pools)
            
            return {
                'total_liquidity': total_liquidity,
                'pools': pools,
                'locked_amount': locked_liquidity,
                'is_sufficient': total_liquidity > self.config['min_liquidity']
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing liquidity: {str(e)}")
            return None
            
    async def execute_trade(self, trade_params: Dict):
        """Execute trade with anti-snipe protection"""
        try:
            # Validate trade parameters
            if not self.validate_trade_params(trade_params):
                return False
                
            # Check risk limits
            if not self.risk_manager.check_trade_risk(trade_params):
                return False
                
            # Anti-snipe checks
            if await self.is_potential_snipe(trade_params):
                self.logger.warning("Potential snipe attempt detected")
                return False
                
            # Execute the trade
            tx_hash = await self.send_transaction(trade_params)
            
            # Monitor transaction
            success = await self.monitor_transaction(tx_hash)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error executing trade: {str(e)}")
            return False
            
    async def is_potential_snipe(self, trade_params: Dict) -> bool:
        """Check for potential sniping conditions"""
        try:
            # Check if token just launched
            if await self.is_new_token(trade_params['token_address']):
                return True
                
            # Check for pending transactions
            if await self.has_suspicious_pending_txs(trade_params['token_address']):
                return True
                
            # Check for price impact
            if self.calculate_price_impact(trade_params) > self.config['max_price_impact']:
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking snipe protection: {str(e)}")
            return True
            
    def calculate_risk_level(self, red_flags: List[str]) -> str:
        """Calculate risk level based on red flags"""
        if len(red_flags) == 0:
            return "LOW"
        elif len(red_flags) <= 2:
            return "MEDIUM"
        else:
            return "HIGH"
            
    async def monitor_portfolio(self):
        """Monitor portfolio performance"""
        try:
            while True:
                # Update portfolio values
                await self.update_portfolio_values()
                
                # Check stop losses
                await self.check_stop_losses()
                
                # Check take profits
                await self.check_take_profits()
                
                # Rebalance if needed
                if await self.should_rebalance():
                    await self.rebalance_portfolio()
                    
                await asyncio.sleep(60)  # Check every minute
                
        except Exception as e:
            self.logger.error(f"Error monitoring portfolio: {str(e)}")
            await asyncio.sleep(60)
            
    async def run_forever(self):
        """Run trading manager continuously"""
        try:
            while True:
                # Update market data
                await self.update_market_data()
                
                # Scan for opportunities
                await self.scan_opportunities()
                
                # Monitor active positions
                await self.monitor_portfolio()
                
                # Update risk parameters
                await self.risk_manager.update_parameters()
                
                await asyncio.sleep(60)  # Update every minute
                
        except Exception as e:
            self.logger.error(f"Error in trading manager: {str(e)}")
            await asyncio.sleep(60)
