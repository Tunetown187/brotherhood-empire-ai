const axios = require('axios');
const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

const NETLIFY_SITE_URL = 'https://ghl-automation-ai.netlify.app';
const TELEGRAM_BOT_TOKEN = '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';

async function setup() {
  try {
    console.log('Brotherhood Empire Bot Setup\n');
    
    // 1. Set up Telegram webhook
    const webhookUrl = `${NETLIFY_SITE_URL}/.netlify/functions/telegram-webhook`;
    
    console.log('\nSetting up Telegram webhook...');
    const response = await axios.get(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=${webhookUrl}`);
    
    if (response.data.ok) {
      console.log('✅ Webhook set successfully!');
      console.log(`Webhook URL: ${webhookUrl}`);
    } else {
      console.error('❌ Failed to set webhook:', response.data.description);
    }

    // 2. Initialize git repository
    console.log('\nInitializing git repository...');
    await execAsync('git init');
    await execAsync('git add .');
    await execAsync('git commit -m "Initial commit: Brotherhood Empire Bot"');

    console.log('\n🎉 Setup completed! Next steps:');
    console.log('\n1. Verify your Netlify deployment settings:');
    console.log('   Site ID: 4129ca4d-69a4-4d42-96cf-a77169ba3a35');
    console.log('   Site URL:', NETLIFY_SITE_URL);
    
    console.log('\n2. Add these environment variables in Netlify:');
    console.log('   TELEGRAM_BOT_TOKEN=7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido');
    console.log('   GHL_API_KEY=your_ghl_api_key');
    console.log('   MAKE_WEBHOOK_URL=your_make_webhook_url');

    console.log('\n3. Test the bot:');
    console.log('   1. Open Telegram');
    console.log('   2. Search for @Brotherhoodempirebot');
    console.log('   3. Send /start command');

  } catch (error) {
    console.error('Error during setup:', error.message);
  }
}

setup();
