"""
Telegram Bot Configuration

To get your API credentials:
1. Go to https://my.telegram.org/apps
2. Create a new application
3. Copy the api_id and api_hash
4. Replace the values below
"""

TELEGRAM_CONFIG = {
    'api_id': 'YOUR_API_ID',  # Replace with your API ID
    'api_hash': 'YOUR_API_HASH',  # Replace with your API hash
    'bot_token': None,  # Optional: Add your bot token if you want to use a bot
    'chat_id': None,  # Will be set automatically to your user ID
}

def update_config(api_id: str, api_hash: str, bot_token: str = None, chat_id: str = None):
    """Update Telegram configuration"""
    global TELEGRAM_CONFIG
    TELEGRAM_CONFIG.update({
        'api_id': api_id,
        'api_hash': api_hash,
        'bot_token': bot_token,
        'chat_id': chat_id
    })
