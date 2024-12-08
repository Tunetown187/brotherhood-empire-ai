import asyncio
import logging
from pathlib import Path
from datetime import datetime
import json
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Import all managers
from automation.content_factory import ContentFactory
from automation.ecommerce_manager import EcommerceManager
from automation.payment_manager import PaymentManager
from automation.lead_gen import LeadGenerator
from automation.campaign_manager import CampaignManager
from automation.affiliate_manager import AffiliateManager
from automation.telegram_bot import SecureTelegramBot
from automation.bhw_scraper import BHWScraper
from automation.security_manager import SecurityManager
from automation.cloud_manager import CloudManager
from automation.crypto_manager import CryptoManager
from automation.defi_manager import DeFiManager
from automation.nft_manager import NFTManager
from automation.metaverse_manager import MetaverseManager
from automation.social_media_manager import SocialMediaManager
from automation.marketing_manager import MarketingManager

class MasterController:
    def __init__(self):
        self.content_factory = ContentFactory()
        self.ecommerce_manager = EcommerceManager()
        self.payment_manager = PaymentManager()
        self.lead_generator = LeadGenerator()
        self.campaign_manager = CampaignManager()
        self.affiliate_manager = AffiliateManager()
        self.telegram_bot = SecureTelegramBot()
        self.bhw_scraper = BHWScraper()
        self.security_manager = SecurityManager()
        self.cloud_manager = CloudManager()
        self.crypto_manager = CryptoManager()
        self.defi_manager = DeFiManager()
        self.nft_manager = NFTManager()
        self.metaverse_manager = MetaverseManager()
        self.social_media_manager = SocialMediaManager()
        self.marketing_manager = MarketingManager()
        
        self.setup_logging()
        self.load_config()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('master_controller.log'),
                logging.StreamHandler()
            ]
        )
        
    def load_config(self):
        config_path = Path(__file__).parent / 'config.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
            
    async def start_all_systems(self):
        """Start all automation systems"""
        try:
            # Start infrastructure
            await self.cloud_manager.setup_servers()
            await self.security_manager.start_monitoring()
            
            # Start revenue generation
            await self.ecommerce_manager.start_stores()
            await self.payment_manager.start_processors()
            await self.content_factory.start_generation()
            await self.affiliate_manager.start_campaigns()
            
            # Start lead generation
            await self.lead_generator.start_scraping()
            await self.campaign_manager.start_campaigns()
            await self.bhw_scraper.start_scraping()
            
            # Start marketing and social media
            await self.social_media_manager.run_forever()
            await self.marketing_manager.run_forever()
            
            # Start crypto operations
            await self.crypto_manager.run_forever()
            await self.defi_manager.run_forever()
            await self.nft_manager.run_forever()
            await self.metaverse_manager.run_forever()
            
            # Start monitoring
            await self.telegram_bot.start()
            
            logging.info("All systems started successfully")
            
        except Exception as e:
            logging.error(f"Error starting systems: {str(e)}")
            await self.telegram_bot.send_notification(f"Error: {str(e)}")
            
    async def monitor_metrics(self):
        """Monitor business metrics"""
        while True:
            metrics = {
                "revenue": await self.payment_manager.get_total_revenue(),
                "leads": await self.lead_generator.get_lead_count(),
                "content": await self.content_factory.get_content_count(),
                "stores": await self.ecommerce_manager.get_store_count()
            }
            
            # Save metrics
            metrics_file = Path("metrics.json")
            with open(metrics_file, "w") as f:
                json.dump(metrics, f, indent=4)
                
            # Send update
            await self.telegram_bot.send_notification(
                f"Daily Metrics:\nRevenue: ${metrics['revenue']}\n" +
                f"Leads: {metrics['leads']}\nContent: {metrics['content']}\n" +
                f"Stores: {metrics['stores']}"
            )
            
            await asyncio.sleep(86400)  # Daily updates
            
    async def run_forever(self):
        """Run all systems continuously"""
        await self.start_all_systems()
        await self.monitor_metrics()
        
if __name__ == "__main__":
    controller = MasterController()
    asyncio.run(controller.run_forever())
