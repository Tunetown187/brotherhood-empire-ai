const axios = require('axios');

// Bot configuration
const token = process.env.TELEGRAM_BOT_TOKEN || '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';
const TELEGRAM_API = `https://api.telegram.org/bot${token}`;

// Helper function to send messages
async function sendTelegramMessage(chatId, text, parse_mode = 'Markdown') {
  try {
    const response = await axios.post(`${TELEGRAM_API}/sendMessage`, {
      chat_id: chatId,
      text: text,
      parse_mode: parse_mode
    });
    console.log('Message sent successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error.response?.data || error.message);
    throw error;
  }
}

// Command handlers
const commandHandlers = {
  '/start': async (chatId) => {
    console.log('Handling /start command for chat:', chatId);
    const message = 'Welcome to Brotherhood Empire Bot! 🏰\n\n' +
      'I am your gateway to the Empire\'s operations. Here are my commands:\n\n' +
      '/status - Check system status\n' +
      '/help - Show this help message\n' +
      '/deploy_agent [name] [role] - Deploy a new agent\n' +
      '/list_agents - List all active agents\n' +
      '/send_command [agent] [command] - Send a command to an agent\n' +
      '/terminate_agent [name] - Terminate an agent';
    
    return sendTelegramMessage(chatId, message);
  },

  '/status': async (chatId) => {
    console.log('Handling /status command for chat:', chatId);
    const message = '✅ *System Status*\n\n' +
      'Bot: Online\n' +
      'Server: Running\n' +
      'Time: ' + new Date().toISOString();
    
    return sendTelegramMessage(chatId, message);
  },

  '/help': async (chatId) => {
    console.log('Handling /help command for chat:', chatId);
    const message = '🤖 *Available Commands*\n\n' +
      '/start - Initialize the bot\n' +
      '/status - Check system status\n' +
      '/help - Show this help message\n' +
      '/deploy_agent [name] [role] - Deploy a new agent\n' +
      '/list_agents - List all active agents\n' +
      '/send_command [agent] [command] - Send a command to an agent\n' +
      '/terminate_agent [name] - Terminate an agent';
    
    return sendTelegramMessage(chatId, message);
  }
};

exports.handler = async function(event, context) {
  console.log('Received webhook event:', event.httpMethod);
  console.log('Headers:', JSON.stringify(event.headers, null, 2));
  
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return { 
      statusCode: 405, 
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  try {
    console.log('Request body:', event.body);
    const data = JSON.parse(event.body);
    console.log('Parsed update:', JSON.stringify(data, null, 2));

    // Handle incoming message
    if (data.message) {
      const chatId = data.message.chat.id;
      const text = data.message.text;
      const username = data.message.from.username;

      console.log(`Received message: "${text}" from chat ${chatId} (${username})`);

      // Handle commands
      if (text && text.startsWith('/')) {
        const command = text.split(' ')[0].toLowerCase();
        console.log('Processing command:', command);
        
        if (commandHandlers[command]) {
          try {
            await commandHandlers[command](chatId);
            console.log('Command handled successfully:', command);
          } catch (error) {
            console.error('Error executing command:', error);
            await sendTelegramMessage(chatId, '❌ Error executing command. Please try again.');
          }
        } else {
          console.log('Unknown command:', command);
          await sendTelegramMessage(chatId, 'Unknown command. Use /help to see available commands.');
        }
      } else {
        console.log('Non-command message received');
        await sendTelegramMessage(chatId, 'Please use commands to interact with me. Send /help to see available commands.');
      }
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ status: 'ok' })
    };
  } catch (error) {
    console.error('Error processing webhook:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        error: 'Error processing message', 
        details: error.message,
        stack: error.stack 
      })
    };
  }
}
