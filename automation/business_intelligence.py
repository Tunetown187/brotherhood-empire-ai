import asyncio
from datetime import datetime
from typing import Dict, List
import sqlite3
import json
import pandas as pd
from pathlib import Path
import aiofiles
from telethon import TelegramClient
import logging

class BusinessIntelligence:
    def __init__(self):
        self.db_path = Path("business_data.db")
        self.setup_database()
        self.telegram_client = None
        self.logger = self.setup_logger()
        
    def setup_logger(self):
        logger = logging.getLogger('business_intelligence')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('business_operations.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
        
    def setup_database(self):
        """Setup SQLite database for business tracking"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Business Operations Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS business_operations (
                id TEXT PRIMARY KEY,
                business_type TEXT,
                platform TEXT,
                revenue REAL,
                costs REAL,
                profit REAL,
                start_date TEXT,
                last_updated TEXT,
                status TEXT,
                performance_metrics TEXT
            )
        ''')
        
        # Financial Transactions
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                business_id TEXT,
                amount REAL,
                type TEXT,
                timestamp TEXT,
                details TEXT,
                FOREIGN KEY (business_id) REFERENCES business_operations (id)
            )
        ''')
        
        # Performance Metrics
        c.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id TEXT PRIMARY KEY,
                business_id TEXT,
                metric_name TEXT,
                metric_value REAL,
                timestamp TEXT,
                FOREIGN KEY (business_id) REFERENCES business_operations (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    async def setup_telegram(self):
        """Setup Telegram client for reporting"""
        self.telegram_client = TelegramClient(
            'business_bot_session',
            api_id="YOUR_API_ID",
            api_hash="YOUR_API_HASH"
        )
        await self.telegram_client.start()
        
    async def track_business(self, business_data: Dict):
        """Track new or update existing business"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        business_id = business_data.get('id')
        
        c.execute('''
            INSERT OR REPLACE INTO business_operations 
            (id, business_type, platform, revenue, costs, profit, start_date, last_updated, status, performance_metrics)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            business_id,
            business_data.get('type'),
            business_data.get('platform'),
            business_data.get('revenue', 0),
            business_data.get('costs', 0),
            business_data.get('profit', 0),
            business_data.get('start_date'),
            datetime.now().isoformat(),
            business_data.get('status'),
            json.dumps(business_data.get('metrics', {}))
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Updated business {business_id}: {business_data}")
        
    async def generate_report(self) -> Dict:
        """Generate comprehensive business report"""
        conn = sqlite3.connect(self.db_path)
        
        # Get overall metrics
        df = pd.read_sql_query('''
            SELECT 
                business_type,
                COUNT(*) as count,
                SUM(revenue) as total_revenue,
                SUM(profit) as total_profit,
                AVG(profit) as avg_profit
            FROM business_operations
            GROUP BY business_type
        ''', conn)
        
        # Get top performing businesses
        top_businesses = pd.read_sql_query('''
            SELECT *
            FROM business_operations
            ORDER BY profit DESC
            LIMIT 5
        ''', conn)
        
        # Get recent transactions
        recent_transactions = pd.read_sql_query('''
            SELECT *
            FROM transactions
            ORDER BY timestamp DESC
            LIMIT 10
        ''', conn)
        
        conn.close()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_metrics': df.to_dict('records'),
            'top_businesses': top_businesses.to_dict('records'),
            'recent_transactions': recent_transactions.to_dict('records')
        }
        
        return report
        
    async def send_telegram_report(self, report: Dict):
        """Send report via Telegram"""
        if not self.telegram_client:
            await self.setup_telegram()
            
        message = f"""🚀 Business Intelligence Report
        
📊 Overall Performance:
Total Revenue: ${sum([m['total_revenue'] for m in report['overall_metrics']]):,.2f}
Total Profit: ${sum([m['total_profit'] for m in report['overall_metrics']]):,.2f}

🏆 Top Performing Businesses:
{self._format_top_businesses(report['top_businesses'])}

💰 Recent Transactions:
{self._format_transactions(report['recent_transactions'])}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        await self.telegram_client.send_message('me', message)
        
    def _format_top_businesses(self, businesses: List[Dict]) -> str:
        return "\n".join([
            f"- {b['business_type']}: ${b['profit']:,.2f} profit"
            for b in businesses
        ])
        
    def _format_transactions(self, transactions: List[Dict]) -> str:
        return "\n".join([
            f"- ${t['amount']:,.2f} ({t['type']})"
            for t in transactions
        ])
        
    async def monitor_efficiency(self):
        """Monitor business efficiency continuously"""
        while True:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Check for underperforming businesses
            c.execute('''
                SELECT *
                FROM business_operations
                WHERE profit < 0
                OR (julianday('now') - julianday(last_updated)) > 7
            ''')
            
            problems = c.fetchall()
            if problems:
                await self.send_telegram_report({
                    'type': 'alert',
                    'businesses': problems
                })
                
            conn.close()
            await asyncio.sleep(3600 * 4)  # Check every 4 hours
