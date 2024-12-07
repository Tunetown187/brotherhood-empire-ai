# Brotherhood Empire Bot

A powerful Telegram bot integrated with Go High Level and Make.com for the Brotherhood Empire AI Agency.

## Features

- Real-time agent status monitoring
- Empire analytics dashboard
- Market analysis
- Integration with Go High Level CRM
- Automated workflows with Make.com
- Secure command handling

## Commands

- `/start` - Initialize the bot
- `/status` - View agents' status
- `/analytics` - View empire analytics
- `/markets` - View active markets
- `/integrations` - Check integration status
- `/ghl_contacts` - View GHL contacts
- `/help` - Show all commands

## Deployment on Netlify

1. Connect your GitHub repository to Netlify

2. Configure environment variables in Netlify:
   - `TELEGRAM_BOT_TOKEN`: 7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido
   - `GHL_API_KEY`: Your Go High Level API key
   - `MAKE_WEBHOOK_URL`: Your Make.com webhook URL

3. Deploy settings:
   - Build command: `npm install`
   - Publish directory: `public`
   - Functions directory: `netlify/functions`

4. After deployment, set up the Telegram webhook:
   ```
   https://api.telegram.org/bot7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido/setWebhook?url=https://your-netlify-site.netlify.app/.netlify/functions/telegram-webhook
   ```

## Integration Setup

### Go High Level
1. Get your API key from Go High Level dashboard
2. Add it to Netlify environment variables
3. Test connection with `/integrations` command

### Make.com
1. Create a new scenario in Make.com
2. Add a webhook trigger
3. Copy the webhook URL
4. Add it to Netlify environment variables
5. Test connection with `/integrations` command

## Security Notes

- Keep all API keys and tokens secure
- Only share bot access with authorized personnel
- Regularly monitor integration status
- Update credentials periodically

## Support

For support or feature requests, contact the Brotherhood Empire development team.
