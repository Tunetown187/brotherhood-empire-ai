from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        
        # Add handlers
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))
    
    def start(self, update, context):
        update.message.reply_text('Brotherhood Empire Bot is online. Ready to serve.')
    
    def echo(self, update, context):
        update.message.reply_text(f"Received: {update.message.text}")
    
    def run(self):
        self.updater.start_polling()
        print("Telegram bot is running...")
        self.updater.idle()
