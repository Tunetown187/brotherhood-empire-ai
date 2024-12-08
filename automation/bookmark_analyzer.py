import json
from pathlib import Path
import sqlite3
from typing import List, Dict
import asyncio
import aiohttp

class BookmarkAnalyzer:
    def __init__(self):
        self.opera_paths = [
            Path("C:/Users/p8tty/AppData/Roaming/Opera Software/Opera Stable"),
            Path("C:/Users/p8tty/AppData/Roaming/Opera Software/Opera GX Stable")
        ]
        self.chrome_paths = [
            Path("C:/Users/p8tty/AppData/Local/Google/Chrome/User Data/Default"),
            Path("C:/Users/p8tty/AppData/Local/Google/Chrome/User Data/Profile 1")
        ]
        self.firefox_paths = [
            Path("C:/Users/p8tty/AppData/Roaming/Mozilla/Firefox/Profiles")
        ]
        self.db_path = Path("bookmarks.db")
        self.setup_database()
        
    def setup_database(self):
        """Setup SQLite database for bookmarks"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id TEXT PRIMARY KEY,
                title TEXT,
                url TEXT,
                category TEXT,
                browser TEXT,
                added_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def parse_opera_bookmarks(self):
        """Parse Opera browser bookmarks"""
        bookmarks = []
        
        for opera_path in self.opera_paths:
            bookmark_file = opera_path / "Bookmarks"
            
            if bookmark_file.exists():
                try:
                    with open(bookmark_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        def process_node(node):
                            if 'type' in node and node['type'] == 'url':
                                bookmarks.append({
                                    'title': node.get('name', ''),
                                    'url': node.get('url', ''),
                                    'category': node.get('category', ''),
                                    'browser': 'Opera',
                                    'date_added': node.get('date_added', '')
                                })
                            
                            if 'children' in node:
                                for child in node['children']:
                                    process_node(child)
                                    
                        # Process bookmark bar and other bookmarks
                        for root in ['bookmark_bar', 'other']:
                            if root in data['roots']:
                                process_node(data['roots'][root])
                except Exception as e:
                    print(f"Error parsing Opera bookmarks at {opera_path}: {str(e)}")
                            
        return bookmarks

    def parse_chrome_bookmarks(self):
        """Parse Chrome browser bookmarks"""
        bookmarks = []
        
        for chrome_path in self.chrome_paths:
            bookmark_file = chrome_path / "Bookmarks"
            
            if bookmark_file.exists():
                try:
                    with open(bookmark_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        def process_node(node):
                            if node.get('type') == 'url':
                                bookmarks.append({
                                    'title': node.get('name', ''),
                                    'url': node.get('url', ''),
                                    'category': '',
                                    'browser': 'Chrome',
                                    'date_added': node.get('date_added', '')
                                })
                            
                            if 'children' in node:
                                for child in node['children']:
                                    process_node(child)
                                    
                        for root in ['bookmark_bar', 'other', 'synced']:
                            if root in data['roots']:
                                process_node(data['roots'][root])
                except Exception as e:
                    print(f"Error parsing Chrome bookmarks at {chrome_path}: {str(e)}")
                    
        return bookmarks

    def parse_firefox_bookmarks(self):
        """Parse Firefox browser bookmarks"""
        bookmarks = []
        
        for firefox_base in self.firefox_paths:
            if firefox_base.exists():
                for profile in firefox_base.glob("*.default*"):
                    places_file = profile / "places.sqlite"
                    if places_file.exists():
                        try:
                            # Create a copy of places.sqlite since Firefox locks it
                            import shutil
                            temp_db = places_file.parent / "places_temp.sqlite"
                            shutil.copy2(places_file, temp_db)
                            
                            conn = sqlite3.connect(temp_db)
                            c = conn.cursor()
                            
                            c.execute("""
                                SELECT b.title, p.url, b.dateAdded 
                                FROM moz_bookmarks b 
                                JOIN moz_places p ON b.fk = p.id 
                                WHERE b.type = 1
                            """)
                            
                            for row in c.fetchall():
                                bookmarks.append({
                                    'title': row[0],
                                    'url': row[1],
                                    'category': '',
                                    'browser': 'Firefox',
                                    'date_added': row[2]
                                })
                                
                            conn.close()
                            temp_db.unlink()  # Delete temporary file
                        except Exception as e:
                            print(f"Error parsing Firefox bookmarks at {profile}: {str(e)}")
                            
        return bookmarks

    async def analyze_bookmark(self, bookmark: Dict):
        """Analyze a bookmark for affiliate opportunities"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(bookmark['url'], timeout=10) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        
                        # Enhanced keyword detection
                        affiliate_keywords = [
                            'affiliate', 'commission', 'cpa', 'offer',
                            'referral', 'partner program', 'join program',
                            'earn money', 'make money', 'passive income',
                            'dropship', 'wholesale', 'resell'
                        ]
                        
                        matches = [k for k in affiliate_keywords if k in text.lower()]
                        if matches:
                            bookmark['category'] = 'affiliate'
                            bookmark['keywords'] = matches
                            
                        # Check for ecommerce opportunities
                        ecommerce_keywords = [
                            'shop', 'store', 'product', 'cart',
                            'checkout', 'buy now', 'purchase',
                            'shipping', 'marketplace'
                        ]
                        
                        ecom_matches = [k for k in ecommerce_keywords if k in text.lower()]
                        if ecom_matches:
                            bookmark['category'] = bookmark.get('category', '') + ',ecommerce'
                            bookmark['ecommerce_keywords'] = ecom_matches
                            
            except Exception as e:
                print(f"Error analyzing bookmark {bookmark['url']}: {str(e)}")
                
    async def analyze_all_bookmarks(self):
        """Analyze all bookmarks for opportunities"""
        all_bookmarks = []
        all_bookmarks.extend(self.parse_opera_bookmarks())
        all_bookmarks.extend(self.parse_chrome_bookmarks())
        all_bookmarks.extend(self.parse_firefox_bookmarks())
        
        print(f"Found {len(all_bookmarks)} bookmarks across all browsers")
        
        # Analyze in batches to avoid overwhelming the system
        batch_size = 10
        for i in range(0, len(all_bookmarks), batch_size):
            batch = all_bookmarks[i:i + batch_size]
            tasks = [self.analyze_bookmark(bookmark) for bookmark in batch]
            await asyncio.gather(*tasks)
            print(f"Analyzed batch {i//batch_size + 1}/{len(all_bookmarks)//batch_size + 1}")
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        for bookmark in all_bookmarks:
            c.execute('''
                INSERT OR REPLACE INTO bookmarks 
                (id, title, url, category, browser, added_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                bookmark['url'],
                bookmark['title'],
                bookmark['url'],
                bookmark.get('category', ''),
                bookmark['browser'],
                bookmark.get('date_added', '')
            ))
            
        conn.commit()
        conn.close()
        
        return all_bookmarks

    def get_business_opportunities(self):
        """Get all identified business opportunities from bookmarks"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT * FROM bookmarks 
            WHERE category LIKE '%affiliate%' 
            OR category LIKE '%ecommerce%'
            ORDER BY added_date DESC
        ''')
        
        opportunities = c.fetchall()
        conn.close()
        
        return opportunities
