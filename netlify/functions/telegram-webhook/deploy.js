const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

// Your bot token
const token = '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';

async function setWebhook(url) {
    try {
        const response = await axios.get(`https://api.telegram.org/bot${token}/setWebhook?url=${url}`);
        console.log('Webhook set response:', response.data);
    } catch (error) {
        console.error('Error setting webhook:', error.response?.data || error.message);
    }
}

// Replace this with your Netlify URL after deployment
const netlifyUrl = process.env.URL || 'https://your-netlify-site.netlify.app';
const webhookUrl = `${netlifyUrl}/.netlify/functions/telegram-webhook`;

setWebhook(webhookUrl);
