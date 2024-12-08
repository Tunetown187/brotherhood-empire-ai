const axios = require('axios');

exports.handler = async function(event, context) {
  try {
    // Only allow POST requests
    if (event.httpMethod !== 'POST') {
      return {
        statusCode: 405,
        body: JSON.stringify({ error: 'Method not allowed' })
      };
    }

    // Parse the incoming webhook data
    const data = JSON.parse(event.body);
    
    // Basic validation
    if (!data || !data.message) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Invalid webhook data' })
      };
    }

    // Handle the message
    const message = data.message;
    const chatId = message.chat.id;
    const text = message.text;

    // Handle commands
    if (text.startsWith('/')) {
      const command = text.split(' ')[0];
      let responseText = '';

      switch (command) {
        case '/start':
          responseText = 'Welcome to Brotherhood Empire Bot! 🚀\n\nI am here to help you manage your crypto empire.';
          break;
        case '/help':
          responseText = 'Available commands:\n/start - Start the bot\n/help - Show this help message';
          break;
        default:
          responseText = 'Unknown command. Type /help to see available commands.';
      }

      // Send response back to Telegram
      await axios.post(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
        chat_id: chatId,
        text: responseText
      });
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Webhook processed successfully' })
    };

  } catch (error) {
    console.error('Webhook error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal server error' })
    };
  }
};
