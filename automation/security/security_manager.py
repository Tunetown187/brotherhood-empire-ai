import logging
from web3 import Web3
from eth_account import Account
import json
from typing import Dict, List
import aiohttp
import asyncio
from datetime import datetime, timedelta

class SecurityManager:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.setup_web3()
        self.known_scams = set()
        self.suspicious_patterns = {}
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SecurityManager')
        
    def load_config(self):
        """Load security configuration"""
        try:
            with open('config/security_config.json', 'r') as f:
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
        
    async def check_contract_security(self, contract_address: str, chain: str) -> Dict:
        """Check contract for common security issues"""
        try:
            w3 = self.w3[chain]
            
            # Get contract code
            code = w3.eth.get_code(contract_address)
            
            security_issues = []
            
            # Check for proxy patterns
            if self.is_proxy_contract(code):
                security_issues.append("Proxy contract detected - verify implementation")
                
            # Check for dangerous functions
            if self.has_dangerous_functions(code):
                security_issues.append("Contains potentially dangerous functions")
                
            # Check for reentrancy vulnerabilities
            if self.check_reentrancy(code):
                security_issues.append("Potential reentrancy vulnerability")
                
            # Check token approval patterns
            if self.check_unsafe_approvals(code):
                security_issues.append("Unsafe approval patterns detected")
                
            return {
                'address': contract_address,
                'chain': chain,
                'issues': security_issues,
                'risk_level': self.calculate_risk_level(security_issues)
            }
            
        except Exception as e:
            self.logger.error(f"Error checking contract security: {str(e)}")
            return None
            
    def is_proxy_contract(self, code: bytes) -> bool:
        """Check if contract is a proxy"""
        proxy_patterns = [
            bytes.fromhex('363d3d373d3d3d363d73'),  # EIP-1167 minimal proxy
            bytes.fromhex('5c3d3d73')  # Custom proxy pattern
        ]
        return any(pattern in code for pattern in proxy_patterns)
        
    def has_dangerous_functions(self, code: bytes) -> bool:
        """Check for dangerous functions"""
        dangerous_patterns = [
            bytes.fromhex('selfdestruct'),
            bytes.fromhex('delegatecall'),
            bytes.fromhex('callcode')
        ]
        return any(pattern in code for pattern in dangerous_patterns)
        
    def check_reentrancy(self, code: bytes) -> bool:
        """Check for reentrancy vulnerabilities"""
        # Look for external calls before state changes
        return False  # Implement detailed check
        
    def check_unsafe_approvals(self, code: bytes) -> bool:
        """Check for unsafe approval patterns"""
        unsafe_patterns = [
            bytes.fromhex('approve(address,uint256)'),
            bytes.fromhex('increaseAllowance(address,uint256)')
        ]
        return any(pattern in code for pattern in unsafe_patterns)
        
    def calculate_risk_level(self, issues: List[str]) -> str:
        """Calculate overall risk level"""
        if len(issues) == 0:
            return "LOW"
        elif len(issues) <= 2:
            return "MEDIUM"
        else:
            return "HIGH"
            
    async def monitor_transactions(self, address: str):
        """Monitor transactions for suspicious patterns"""
        try:
            while True:
                for chain, w3 in self.w3.items():
                    # Get latest transactions
                    txns = await self.get_recent_transactions(address, chain)
                    
                    for tx in txns:
                        if await self.is_suspicious_transaction(tx):
                            await self.alert_suspicious_activity(tx)
                            
                await asyncio.sleep(10)  # Check every 10 seconds
                
        except Exception as e:
            self.logger.error(f"Error monitoring transactions: {str(e)}")
            
    async def is_suspicious_transaction(self, tx: Dict) -> bool:
        """Check if transaction is suspicious"""
        red_flags = []
        
        # Check for known scam addresses
        if tx['to'] in self.known_scams:
            red_flags.append("Known scam address")
            
        # Check for unusual gas prices
        if self.is_unusual_gas(tx['gasPrice']):
            red_flags.append("Unusual gas price")
            
        # Check for honeypot patterns
        if await self.check_honeypot_pattern(tx):
            red_flags.append("Potential honeypot")
            
        return len(red_flags) > 0
        
    async def check_honeypot_pattern(self, tx: Dict) -> bool:
        """Check for honeypot contract patterns"""
        try:
            # Check if contract prevents selling
            # Check for hidden fees
            # Check for ownership concentration
            return False  # Implement detailed checks
            
        except Exception as e:
            self.logger.error(f"Error checking honeypot: {str(e)}")
            return False
            
    def is_unusual_gas(self, gas_price: int) -> bool:
        """Check if gas price is unusual"""
        # Implement gas price analysis
        return False
        
    async def alert_suspicious_activity(self, tx: Dict):
        """Alert about suspicious activity"""
        self.logger.warning(f"Suspicious transaction detected: {tx['hash']}")
        
        # Implement alert system (Discord, Telegram, etc.)
        
    async def run_forever(self):
        """Run security monitoring continuously"""
        try:
            while True:
                # Update known scams list
                await self.update_scam_database()
                
                # Monitor for new attack vectors
                await self.monitor_attack_vectors()
                
                # Update security rules
                await self.update_security_rules()
                
                await asyncio.sleep(3600)  # Update every hour
                
        except Exception as e:
            self.logger.error(f"Error in security monitor: {str(e)}")
            await asyncio.sleep(60)
