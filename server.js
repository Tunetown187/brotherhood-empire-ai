const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = process.env.PORT || 3000;

// Bot configuration
const token = '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';
const TELEGRAM_API = `https://api.telegram.org/bot${token}`;

app.use(bodyParser.json());

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

app.post('/webhook', async (req, res) => {
  console.log('Received webhook event');
  console.log('Request body:', JSON.stringify(req.body, null, 2));

  try {
    // Handle incoming message
    if (req.body.message) {
      const chatId = req.body.message.chat.id;
      const text = req.body.message.text;
      const username = req.body.message.from.username;

      console.log(`Received message: "${text}" from chat ${chatId} (${username})`);

      // Handle commands
      if (text && text.startsWith('/')) {
        const parts = text.split(' ');
        const command = parts[0].toLowerCase();
        const args = parts.slice(1);
        console.log('Processing command:', command, 'with args:', args);
        
        if (commandHandlers[command]) {
          try {
            await commandHandlers[command](chatId, args);
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

    res.status(200).json({ status: 'ok' });
  } catch (error) {
    console.error('Error processing webhook:', error);
    res.status(500).json({ 
      error: 'Error processing message', 
      details: error.message 
    });
  }
});

// Start the server
app.listen(port, async () => {
  console.log(`Server is running on port ${port}`);
  
  // Set webhook to our local server (requires ngrok or similar for production)
  try {
    const response = await axios.post(`${TELEGRAM_API}/setWebhook`, {
      url: `https://brotherhood-empire-bot.netlify.app/webhook`
    });
    console.log('Webhook set:', response.data);
  } catch (error) {
    console.error('Error setting webhook:', error.response?.data || error.message);
  }
});
