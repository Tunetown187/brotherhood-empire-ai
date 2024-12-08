import asyncio
from automation.cloud_manager import CloudManager
from automation.ecommerce_manager import EcommerceManager
from automation.affiliate_manager import AffiliateManager
from automation.lead_gen import LeadGenerator
from automation.telegram_bot import SecureTelegramBot

class AutomationOrchestrator:
    def __init__(self):
        self.cloud = CloudManager()
        self.ecommerce = EcommerceManager()
        self.affiliate = AffiliateManager()
        self.lead_gen = LeadGenerator()
        self.telegram = SecureTelegramBot()
        
    async def start_all_services(self):
        """Start all automation services"""
        # Deploy to cloud
        services = ['ecommerce', 'affiliate', 'lead_gen']
        for service in services:
            await self.cloud.deploy_service(service, Path(f'./dockerfiles/{service}.dockerfile'))
            
        # Start monitoring
        asyncio.create_task(self.cloud.monitor_services())
        
        # Start Telegram bot
        asyncio.create_task(self.telegram.run())
        
        # Run continuous operations
        while True:
            try:
                # Manage dropshipping stores
                for store_url in self.ecommerce.stores:
                    await self.ecommerce.manage_store(store_url, {})
                    
                # Run affiliate campaigns
                await self.affiliate.optimize_campaigns()
                
                # Generate leads
                await self.lead_gen.run_campaign({})
                
                await asyncio.sleep(3600)  # Run every hour
                
            except Exception as e:
                await self.telegram.send_notification(f"Error in automation: {str(e)}")

if __name__ == "__main__":
    orchestrator = AutomationOrchestrator()
    asyncio.run(orchestrator.start_all_services())
