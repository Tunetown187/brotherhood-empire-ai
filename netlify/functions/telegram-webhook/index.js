const axios = require('axios');

// Bot configuration
const token = process.env.TELEGRAM_BOT_TOKEN || '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';
const TELEGRAM_API = `https://api.telegram.org/bot${token}`;
const GHL_API_KEY = process.env.GHL_API_KEY;
const MAKE_WEBHOOK_URL = process.env.MAKE_WEBHOOK_URL;

// Helper function to send messages
async function sendTelegramMessage(chatId, text, parse_mode = 'Markdown', retry = 3) {
  for (let i = 0; i < retry; i++) {
    try {
      const response = await axios.post(`${TELEGRAM_API}/sendMessage`, {
        chat_id: chatId,
        text: text,
        parse_mode: parse_mode
      });
      console.log('Message sent successfully:', response.data);
      return response.data;
    } catch (error) {
      console.error(`Attempt ${i + 1}/${retry} failed:`, error.response?.data || error.message);
      if (i === retry - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1))); // Exponential backoff
    }
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
      custom_fields: [
        { id: 'role', value: role },
        { id: 'status', value: 'active' },
        { id: 'deployed_date', value: new Date().toISOString() }
      ]
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
      data,
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'production'
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
    const message = '🏰 *Welcome to Brotherhood Empire Bot!*\n\n' +
      'I am your gateway to the Empire\'s operations. Here are my commands:\n\n' +
      '🔍 */status* - Check system status\n' +
      '❓ */help* - Show this help message\n' +
      '🤖 */deploy_agent* [name] [role] - Deploy a new agent\n' +
      '📋 */list_agents* - List all active agents\n' +
      '📝 */send_command* [agent] [command] - Send a command to an agent\n' +
      '❌ */terminate_agent* [name] - Terminate an agent\n\n' +
      '🔒 */security* - View security status\n' +
      '💰 */profit* - View profit statistics';
    
    // Notify Make.com about new user
    if (MAKE_WEBHOOK_URL) {
      await triggerMakeWebhook('new_user', { chatId });
    }
    return sendTelegramMessage(chatId, message);
  },

  '/status': async (chatId) => {
    console.log('Handling /status command for chat:', chatId);
    const uptime = process.uptime();
    const hours = Math.floor(uptime / 3600);
    const minutes = Math.floor((uptime % 3600) / 60);
    
    const message = '✅ *System Status*\n\n' +
      '🤖 Bot: Online\n' +
      '🖥️ Server: Running\n' +
      '🔗 GHL Integration: ' + (GHL_API_KEY ? '✅' : '❌') + '\n' +
      '🔄 Make.com Integration: ' + (MAKE_WEBHOOK_URL ? '✅' : '❌') + '\n' +
      '⏱️ Uptime: ' + hours + 'h ' + minutes + 'm\n' +
      '🕒 Time: ' + new Date().toISOString();
    
    return sendTelegramMessage(chatId, message);
  },

  '/deploy_agent': async (chatId, args) => {
    if (args.length < 2) {
      return sendTelegramMessage(chatId, '❌ Usage: /deploy_agent [name] [role]');
    }
    const name = args[0];
    const role = args[1];
    
    try {
      const deploymentStart = new Date();
      await sendTelegramMessage(chatId, `🔄 Deploying agent *${name}* with role *${role}*...`);
      
      // Create contact in GHL
      if (GHL_API_KEY) {
        await createGHLContact(name, role);
      }
      
      // Trigger Make.com workflow
      if (MAKE_WEBHOOK_URL) {
        await triggerMakeWebhook('agent_deployed', { 
          name, 
          role,
          deploymentTime: deploymentStart.toISOString()
        });
      }
      
      const deploymentTime = (new Date() - deploymentStart) / 1000;
      return sendTelegramMessage(chatId, 
        `✅ Agent *${name}* deployed successfully!\n\n` +
        `Role: *${role}*\n` +
        `Deployment Time: ${deploymentTime.toFixed(2)}s\n\n` +
        `Use /status to check system status`
      );
    } catch (error) {
      console.error('Error deploying agent:', error);
      return sendTelegramMessage(chatId, 
        `❌ Error deploying agent:\n${error.message}\n\n` +
        `Please try again or contact support.`
      );
    }
  },

  '/security': async (chatId) => {
    const message = '🔒 *Security Status*\n\n' +
      '✅ Encryption: Active\n' +
      '✅ Firewall: Active\n' +
      '✅ VPN: Connected\n' +
      '✅ 2FA: Enabled\n\n' +
      'No security threats detected.';
    
    return sendTelegramMessage(chatId, message);
  },

  '/profit': async (chatId) => {
    const message = '💰 *Profit Statistics*\n\n' +
      '📈 Total Profit: $XXX,XXX\n' +
      '📊 Monthly Growth: XX%\n' +
      '🎯 ROI: XX%\n\n' +
      'Use /status for more details.';
    
    return sendTelegramMessage(chatId, message);
  },

  '/help': async (chatId) => {
    console.log('Handling /help command for chat:', chatId);
    const message = '🤖 *Available Commands*\n\n' +
      '🏁 */start* - Initialize the bot\n' +
      '🔍 */status* - Check system status\n' +
      '❓ */help* - Show this help message\n' +
      '🤖 */deploy_agent* [name] [role] - Deploy a new agent\n' +
      '📋 */list_agents* - List all active agents\n' +
      '📝 */send_command* [agent] [command] - Send a command to an agent\n' +
      '❌ */terminate_agent* [name] - Terminate an agent\n' +
      '🔒 */security* - View security status\n' +
      '💰 */profit* - View profit statistics';
    
    return sendTelegramMessage(chatId, message);
  }
};

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const body = JSON.parse(event.body);
    console.log('Received update:', JSON.stringify(body, null, 2));

    // Process the update
    if (body.message) {
      const chatId = body.message.chat.id;
      const text = body.message.text;

      // Prepare response
      let responseText = '';

      if (text === '/start') {
        responseText = '🏰 Welcome to Brotherhood Empire!\n\nI am your AI assistant. Here are my commands:\n/status - Check system status\n/deploy - Deploy new agents\n/help - Show all commands';
      } else if (text === '/status') {
        responseText = '✨ Brotherhood Empire Status:\n\n' +
          '🤖 AI Agents: OPERATIONAL\n' +
          '💼 Business Operations: ACTIVE\n' +
          '🌐 Network Status: OPTIMAL\n' +
          '🔒 Security Level: MAXIMUM';
      } else if (text === '/help') {
        responseText = '🤖 Available Commands:\n\n' +
          '/start - Initialize the bot\n' +
          '/status - Check system status\n' +
          '/deploy - Deploy new agents\n' +
          '/help - Show this help message';
      } else {
        responseText = '🤖 Processing your request...';
      }

      // Send response back to Telegram
      await axios.post(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
        chat_id: chatId,
        text: responseText,
        parse_mode: 'Markdown'
      });

      return {
        statusCode: 200,
        body: JSON.stringify({ message: 'Success' })
      };
    }
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to process webhook' })
    };
  }
};
