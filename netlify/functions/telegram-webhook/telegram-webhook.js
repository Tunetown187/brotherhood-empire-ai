const axios = require('axios');

// Bot configuration
const token = process.env.TELEGRAM_BOT_TOKEN || '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';
const TELEGRAM_API = `https://api.telegram.org/bot${token}`;
const GHL_API_KEY = process.env.GHL_API_KEY;
const MAKE_WEBHOOK_URL = process.env.MAKE_WEBHOOK_URL;

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

// GHL Helper Functions
async function createGHLContact(name, role) {
  if (!GHL_API_KEY) {
    throw new Error('GHL_API_KEY not configured');
  }
  try {
    const response = await axios.post('https://rest.gohighlevel.com/v1/contacts/', {
      name: name,
      custom_fields: [{ id: 'role', value: role }]
    }, {
      headers: { 'Authorization': `Bearer ${GHL_API_KEY}` }
    });
    return response.data;
  } catch (error) {
    console.error('Error creating GHL contact:', error);
    throw error;
  }
}

// Make.com Helper Functions
async function triggerMakeWebhook(eventType, data) {
  if (!MAKE_WEBHOOK_URL) {
    throw new Error('MAKE_WEBHOOK_URL not configured');
  }
  try {
    const response = await axios.post(MAKE_WEBHOOK_URL, {
      eventType,
      data
    });
    return response.data;
  } catch (error) {
    console.error('Error triggering Make webhook:', error);
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
    
    // Notify Make.com about new user
    await triggerMakeWebhook('new_user', { chatId });
    return sendTelegramMessage(chatId, message);
  },

  '/status': async (chatId) => {
    console.log('Handling /status command for chat:', chatId);
    const message = '✅ *System Status*\n\n' +
      'Bot: Online\n' +
      'Server: Running\n' +
      'GHL Integration: ' + (GHL_API_KEY ? '✅' : '❌') + '\n' +
      'Make.com Integration: ' + (MAKE_WEBHOOK_URL ? '✅' : '❌') + '\n' +
      'Time: ' + new Date().toISOString();
    
    return sendTelegramMessage(chatId, message);
  },

  '/deploy_agent': async (chatId, args) => {
    if (args.length < 2) {
      return sendTelegramMessage(chatId, 'Usage: /deploy_agent [name] [role]');
    }
    const name = args[0];
    const role = args[1];
    
    try {
      // Create contact in GHL
      await createGHLContact(name, role);
      
      // Trigger Make.com workflow
      await triggerMakeWebhook('agent_deployed', { name, role });
      
      return sendTelegramMessage(chatId, `✅ Agent *${name}* deployed successfully as *${role}*`);
    } catch (error) {
      console.error('Error deploying agent:', error);
      return sendTelegramMessage(chatId, `❌ Error deploying agent: ${error.message}`);
    }
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
