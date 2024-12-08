const axios = require('axios');

// Your bot token
const token = process.env.TELEGRAM_BOT_TOKEN || '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';

async function deleteWebhook() {
    try {
        const response = await axios.get(`https://api.telegram.org/bot${token}/deleteWebhook`);
        console.log('Webhook deleted:', response.data);
    } catch (error) {
        console.error('Error deleting webhook:', error.response?.data || error.message);
    }
}

async function setWebhook(url) {
    try {
        // First, delete any existing webhook
        await deleteWebhook();
        
        // Set the new webhook
        const response = await axios.get(`https://api.telegram.org/bot${token}/setWebhook?url=${url}&drop_pending_updates=true`);
        console.log('Webhook set response:', response.data);
        
        // Get webhook info
        const infoResponse = await axios.get(`https://api.telegram.org/bot${token}/getWebhookInfo`);
        console.log('\nWebhook info:', infoResponse.data);

        // Test the bot's ability to send messages
        const testMessage = '🔄 Bot redeployed and webhook updated!';
        const sendMessageResponse = await axios.post(`https://api.telegram.org/bot${token}/sendMessage`, {
            chat_id: process.env.ADMIN_CHAT_ID || '5085462345', // Your chat ID
            text: testMessage,
            parse_mode: 'Markdown'
        });
        console.log('\nTest message sent:', sendMessageResponse.data);
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

// Your Netlify URL
const netlifyUrl = 'https://inquisitive-phoenix-3ebc6f.netlify.app';
const webhookUrl = `${netlifyUrl}/.netlify/functions/telegram-webhook`;

console.log(`Setting webhook URL to: ${webhookUrl}`);
setWebhook(webhookUrl);
