const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

// Initialize bot
const token = '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';
const bot = new TelegramBot(token);

// Command handlers
const commandHandlers = {
  '/start': async (chatId) => {
    const message = 'Welcome to Brotherhood Empire Bot! 🏰\n\n' +
      'I am your gateway to the Empire\'s operations. Here are my commands:\n\n' +
      '/status - Check system status\n' +
      '/help - Show this help message';
    
    return bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });
  },

  '/status': async (chatId) => {
    const message = '✅ *System Status*\n\n' +
      'Bot: Online\n' +
      'Server: Running\n' +
      'Time: ' + new Date().toISOString();
    
    return bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });
  },

  '/help': async (chatId) => {
    const message = '🤖 *Available Commands*\n\n' +
      '/start - Initialize the bot\n' +
      '/status - Check system status\n' +
      '/help - Show this help message';
    
    return bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });
  }
};

exports.handler = async function(event, context) {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const data = JSON.parse(event.body);
    console.log('Received update:', JSON.stringify(data));

    // Handle incoming message
    if (data.message) {
      const chatId = data.message.chat.id;
      const text = data.message.text;

      console.log(`Received message: ${text} from chat ${chatId}`);

      // Handle commands
      if (text && text.startsWith('/')) {
        const command = text.split(' ')[0].toLowerCase();
        if (commandHandlers[command]) {
          await commandHandlers[command](chatId);
        } else {
          await bot.sendMessage(chatId, 'Unknown command. Use /help to see available commands.');
        }
      } else {
        await bot.sendMessage(chatId, 'Please use commands to interact with me. Send /help to see available commands.');
      }
    }

    return {
      statusCode: 200,
      body: 'OK'
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Error processing message', details: error.message })
    };
  }
}
