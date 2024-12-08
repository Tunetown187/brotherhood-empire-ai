import asyncio
from telethon import TelegramClient, events
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.secure_config import SecureConfig

class SecureTelegramBot:
    def __init__(self):
        self.config = SecureConfig()
        self.api_id = "YOUR_API_ID"  # Replace with your API ID
        self.api_hash = "YOUR_API_HASH"  # Replace with your API Hash
        self.bot_token = self.config.get_api_key('TELEGRAM_BOT')
        self.client = None
        
    async def start(self):
        self.client = TelegramClient('bot_session', self.api_id, self.api_hash)
        await self.client.start(bot_token=self.bot_token)
        
        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            await event.respond('Bot started securely')
            
        @self.client.on(events.NewMessage(pattern='/status'))
        async def status_handler(event):
            await event.respond('System running anonymously')
            
    async def send_notification(self, message: str):
        if self.client:
            # Send to admin chat
            await self.client.send_message('me', message)
            
    async def run(self):
        await self.start()
        await self.client.run_until_disconnected()
