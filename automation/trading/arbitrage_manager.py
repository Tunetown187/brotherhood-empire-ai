import asyncio
import logging
from web3 import Web3
from typing import Dict, List
import json
from decimal import Decimal
from eth_abi import encode_abi
import networkx as nx

class ArbitrageManager:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.setup_web3()
        self.setup_contracts()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('ArbitrageManager')
        
    def load_config(self):
        """Load arbitrage configuration"""
        try:
            with open('config/arbitrage_config.json', 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            self.config = {}
            
    def setup_web3(self):
        """Setup Web3 connections"""
        self.w3 = {
            'eth': Web3(Web3.HTTPProvider(self.config['eth_rpc'])),
            'bsc': Web3(Web3.HTTPProvider(self.config['bsc_rpc'])),
            'polygon': Web3(Web3.HTTPProvider(self.config['polygon_rpc']))
        }
        
    def setup_contracts(self):
        """Setup smart contract interfaces"""
        # Load contract ABIs
        with open('contracts/abi/FlashArbitrage.json', 'r') as f:
            flash_arb_abi = json.load(f)
            
        # Initialize contract instances
        self.contracts = {
            'flash_arbitrage': self.w3['eth'].eth.contract(
                address=self.config['flash_arbitrage_address'],
                abi=flash_arb_abi
            )
        }
        
    async def find_arbitrage_opportunities(self) -> List[Dict]:
        """Find arbitrage opportunities across DEXes"""
        try:
            opportunities = []
            
            # Get prices from all DEXes
            prices = await self.get_all_prices()
            
            # Build price graph
            graph = self.build_price_graph(prices)
            
            # Find negative cycles (arbitrage opportunities)
            cycles = self.find_negative_cycles(graph)
            
            for cycle in cycles:
                opportunity = await self.analyze_opportunity(cycle, prices)
                if opportunity['profit'] > self.config['min_profit']:
                    opportunities.append(opportunity)
                    
            return opportunities
            
        except Exception as e:
            self.logger.error(f"Error finding opportunities: {str(e)}")
            return []
            
    def build_price_graph(self, prices: Dict) -> nx.DiGraph:
        """Build a directed graph of prices"""
        G = nx.DiGraph()
        
        for token1 in prices:
            for token2 in prices[token1]:
                for dex in prices[token1][token2]:
                    # Add edge with negative log price for Bellman-Ford
                    weight = -1 * float(prices[token1][token2][dex])
                    G.add_edge(
                        token1,
                        token2,
                        weight=weight,
                        dex=dex
                    )
                    
        return G
        
    def find_negative_cycles(self, G: nx.DiGraph) -> List[List[str]]:
        """Find negative cycles in price graph"""
        cycles = []
        
        try:
            # Use Bellman-Ford to detect negative cycles
            for source in G.nodes():
                try:
                    nx.bellman_ford_predecessor_and_distance(G, source)
                except nx.NetworkXUnboundedShortestPath:
                    # Negative cycle detected
                    cycle = self.extract_negative_cycle(G, source)
                    if cycle:
                        cycles.append(cycle)
                        
        except Exception as e:
            self.logger.error(f"Error finding negative cycles: {str(e)}")
            
        return cycles
        
    async def analyze_opportunity(self, cycle: List[str], prices: Dict) -> Dict:
        """Analyze profitability of arbitrage opportunity"""
        try:
            # Calculate optimal trade size
            size = await self.calculate_optimal_size(cycle, prices)
            
            # Calculate expected profit
            profit = await self.calculate_profit(cycle, size, prices)
            
            # Calculate gas costs
            gas_cost = await self.estimate_gas_cost(cycle, size)
            
            # Calculate net profit
            net_profit = profit - gas_cost
            
            return {
                'cycle': cycle,
                'size': size,
                'profit': net_profit,
                'gas_cost': gas_cost,
                'path': self.format_trade_path(cycle)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing opportunity: {str(e)}")
            return None
            
    async def execute_arbitrage(self, opportunity: Dict) -> bool:
        """Execute arbitrage trade"""
        try:
            # Prepare transaction data
            path1, path2 = self.split_path(opportunity['path'])
            
            params = encode_abi(
                ['address[]', 'address[]', 'uint256'],
                [path1, path2, opportunity['profit']]
            )
            
            # Execute flash loan arbitrage
            tx_hash = await self.contracts['flash_arbitrage'].functions.executeArbitrage(
                opportunity['cycle'][0],
                opportunity['size'],
                params
            ).transact()
            
            # Wait for confirmation
            receipt = await self.w3['eth'].eth.wait_for_transaction_receipt(tx_hash)
            
            return receipt.status == 1
            
        except Exception as e:
            self.logger.error(f"Error executing arbitrage: {str(e)}")
            return False
            
    async def monitor_opportunities(self):
        """Monitor for arbitrage opportunities"""
        try:
            while True:
                # Find opportunities
                opportunities = await self.find_arbitrage_opportunities()
                
                for opp in opportunities:
                    # Verify opportunity still exists
                    if await self.verify_opportunity(opp):
                        # Execute arbitrage
                        success = await self.execute_arbitrage(opp)
                        
                        if success:
                            self.logger.info(
                                f"Successfully executed arbitrage: {opp['profit']} ETH profit"
                            )
                            
                await asyncio.sleep(1)  # Check every block
                
        except Exception as e:
            self.logger.error(f"Error monitoring opportunities: {str(e)}")
            await asyncio.sleep(60)
            
    async def run_forever(self):
        """Run arbitrage manager continuously"""
        try:
            while True:
                # Monitor for opportunities
                await self.monitor_opportunities()
                
                # Update price feeds
                await self.update_price_feeds()
                
                # Clean up pending transactions
                await self.cleanup_pending()
                
                await asyncio.sleep(1)  # Update every block
                
        except Exception as e:
            self.logger.error(f"Error in arbitrage manager: {str(e)}")
            await asyncio.sleep(60)
