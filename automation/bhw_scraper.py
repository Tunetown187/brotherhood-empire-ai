import asyncio
from typing import Dict, List
import aiohttp
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import json
from pathlib import Path

class BHWScraper:
    def __init__(self):
        self.db_path = Path("seo_techniques.db")
        self.setup_database()
        self.categories = [
            'seo-tools-and-programs',
            'black-hat-seo',
            'white-hat-seo',
            'social-media-marketing',
            'affiliate-marketing',
            'ecommerce'
        ]
        
    def setup_database(self):
        """Setup database for SEO techniques"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # SEO Techniques
        c.execute('''
            CREATE TABLE IF NOT EXISTS seo_techniques (
                id TEXT PRIMARY KEY,
                title TEXT,
                category TEXT,
                content TEXT,
                url TEXT,
                votes INTEGER,
                replies INTEGER,
                collected_date TEXT
            )
        ''')
        
        # Implemented Techniques
        c.execute('''
            CREATE TABLE IF NOT EXISTS implemented_techniques (
                id TEXT PRIMARY KEY,
                technique_id TEXT,
                implementation_date TEXT,
                success_rate REAL,
                notes TEXT,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    async def scrape_bhw(self):
        """Scrape BlackHatWorld for SEO techniques"""
        async with aiohttp.ClientSession() as session:
            for category in self.categories:
                try:
                    url = f"https://www.blackhatworld.com/{category}"
                    async with session.get(url) as response:
                        if response.status == 200:
                            html = await response.text()
                            await self.parse_category_page(html, category)
                            
                except Exception as e:
                    print(f"Error scraping category {category}: {str(e)}")
                    
                await asyncio.sleep(5)  # Be nice to the server
                
    async def parse_category_page(self, html: str, category: str):
        """Parse category page for threads"""
        soup = BeautifulSoup(html, 'html.parser')
        threads = soup.find_all('div', class_='thread')
        
        for thread in threads:
            try:
                thread_data = {
                    'id': thread.get('id', ''),
                    'title': thread.find('h3').text.strip(),
                    'category': category,
                    'url': thread.find('a')['href'],
                    'votes': int(thread.find('span', class_='votes').text),
                    'replies': int(thread.find('span', class_='replies').text)
                }
                
                # Get thread content
                content = await self.get_thread_content(thread_data['url'])
                if content:
                    thread_data['content'] = content
                    await self.store_technique(thread_data)
                    
            except Exception as e:
                print(f"Error parsing thread: {str(e)}")
                
    async def get_thread_content(self, url: str) -> str:
        """Get thread content"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        content = soup.find('div', class_='post-content')
                        return content.text.strip() if content else ""
                        
            except Exception as e:
                print(f"Error getting thread content: {str(e)}")
                
            return ""
            
    async def store_technique(self, technique: Dict):
        """Store SEO technique in database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                INSERT OR REPLACE INTO seo_techniques
                (id, title, category, content, url, votes, replies, collected_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                technique['id'],
                technique['title'],
                technique['category'],
                technique.get('content', ''),
                technique['url'],
                technique['votes'],
                technique['replies'],
                datetime.now().isoformat()
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"Error storing technique: {str(e)}")
            
        finally:
            conn.close()
            
    async def get_top_techniques(self) -> List[Dict]:
        """Get top SEO techniques"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                SELECT * FROM seo_techniques
                WHERE votes > 10
                ORDER BY votes DESC, replies DESC
                LIMIT 50
            ''')
            
            techniques = c.fetchall()
            return [
                {
                    'id': t[0],
                    'title': t[1],
                    'category': t[2],
                    'content': t[3],
                    'url': t[4],
                    'votes': t[5],
                    'replies': t[6]
                }
                for t in techniques
            ]
            
        finally:
            conn.close()
            
    async def implement_technique(self, technique_id: str, notes: str):
        """Mark technique as implemented"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                INSERT INTO implemented_techniques
                (id, technique_id, implementation_date, success_rate, notes, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                f"impl_{technique_id}",
                technique_id,
                datetime.now().isoformat(),
                0.0,  # Initial success rate
                notes,
                'active'
            ))
            
            conn.commit()
            
        finally:
            conn.close()
            
    async def update_technique_success(self, technique_id: str, success_rate: float):
        """Update success rate of implemented technique"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                UPDATE implemented_techniques
                SET success_rate = ?
                WHERE technique_id = ?
            ''', (success_rate, technique_id))
            
            conn.commit()
            
        finally:
            conn.close()
            
    async def run_forever(self):
        """Run scraper continuously"""
        while True:
            try:
                await self.scrape_bhw()
                
                # Get and analyze top techniques
                techniques = await self.get_top_techniques()
                
                # Log findings
                with open('logs/seo_techniques.log', 'a') as f:
                    f.write(f"\n--- {datetime.now().isoformat()} ---\n")
                    f.write(f"Found {len(techniques)} top techniques\n")
                    for t in techniques[:5]:  # Log top 5
                        f.write(f"- {t['title']} (Votes: {t['votes']})\n")
                        
            except Exception as e:
                print(f"Error in main scraper loop: {str(e)}")
                
            await asyncio.sleep(3600 * 6)  # Run every 6 hours
