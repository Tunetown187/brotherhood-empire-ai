const axios = require('axios');
const { exec } = require('child_process');
const util = require('util');
const fs = require('fs').promises;
const path = require('path');
const execAsync = util.promisify(exec);

const NETLIFY_SITE_URL = 'https://ghl-automation-ai.netlify.app';
const TELEGRAM_BOT_TOKEN = '7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido';

// Netlify Configuration
process.env.NETLIFY_AUTH_TOKEN = 'nfp_M3s5cHYq5ZFmEP6F7iyvra832ykWULYC9286';
process.env.NETLIFY_SITE_ID = '05718948-f2fe-47e6-80a1-e32f1b20d5fe';

// Stripe Configuration
process.env.STRIPE_SECRET_KEY = 'YOUR_STRIPE_SECRET_KEY';
process.env.STRIPE_PUBLISHABLE_KEY = 'YOUR_STRIPE_PUBLISHABLE_KEY';
process.env.STRIPE_WEBHOOK_SECRET = 'YOUR_STRIPE_WEBHOOK_SECRET';

// GoHighLevel Integration for Payments
const GHL_CONFIG = {
  apiKey: process.env.GHL_API_KEY,
  location: process.env.GHL_LOCATION_ID || 'default',
  paymentProcessor: 'stripe'
};

// Payment Configuration using GoHighLevel
const PAYMENT_CONFIG = {
  useGHL: true,
  packages: {
    basic: {
      name: 'Basic Package',
      price: 997,
      features: ['Lead Generation', 'Basic Automation', 'Email Marketing'],
      ghlProductId: 'YOUR_GHL_BASIC_PRODUCT_ID'
    },
    premium: {
      name: 'Premium Package',
      price: 1997,
      features: ['Advanced Automation', 'Full Marketing Suite', 'Priority Support'],
      ghlProductId: 'YOUR_GHL_PREMIUM_PRODUCT_ID'
    },
    enterprise: {
      name: 'Enterprise Package',
      price: 4997,
      features: ['Custom Solutions', 'Dedicated Account Manager', 'White Label'],
      ghlProductId: 'YOUR_GHL_ENTERPRISE_PRODUCT_ID'
    }
  },
  cryptoEnabled: true,
  cryptoWallet: 'YOUR_CRYPTO_WALLET_ADDRESS'
};

// Initialize GHL API client
const initGHLPayments = async () => {
  try {
    const axios = require('axios');
    const ghlClient = axios.create({
      baseURL: 'https://rest.gohighlevel.com/v1/',
      headers: {
        'Authorization': `Bearer ${GHL_CONFIG.apiKey}`,
        'Content-Type': 'application/json'
      }
    });

    // Verify GHL connection
    const response = await ghlClient.get('locations/');
    console.log('✅ GoHighLevel connection established');
    return ghlClient;
  } catch (error) {
    console.error('❌ Error connecting to GoHighLevel:', error.message);
    throw error;
  }
};

module.exports = { 
  PAYMENT_CONFIG,
  GHL_CONFIG,
  initGHLPayments
};

async function checkDependencies() {
  console.log('\n📦 Checking dependencies...');
  
  try {
    await execAsync('git --version');
    console.log('✅ Git installed');
  } catch {
    throw new Error('Git is required but not installed. Please install Git first.');
  }
}

async function setupWebhook() {
  console.log('\n🔄 Setting up Telegram webhook...');
  
  const webhookUrl = `${NETLIFY_SITE_URL}/.netlify/functions/telegram-webhook`;
  
  // First delete any existing webhook
  console.log('Removing existing webhook...');
  await axios.get(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/deleteWebhook`);
  
  // Set new webhook
  console.log(`Setting webhook URL to: ${webhookUrl}`);
  const response = await axios.get(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=${webhookUrl}`);
  
  if (response.data.ok) {
    console.log('✅ Webhook set successfully!');
  } else {
    throw new Error(`Failed to set webhook: ${response.data.description}`);
  }
  
  // Verify webhook
  const infoResponse = await axios.get(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo`);
  console.log('\nWebhook verification:', JSON.stringify(infoResponse.data, null, 2));
  
  return infoResponse.data;
}

async function setupGit() {
  console.log('\n📂 Setting up Git repository...');
  
  try {
    await execAsync('git rev-parse --is-inside-work-tree');
    console.log('✅ Git repository already initialized');
  } catch {
    console.log('Initializing new Git repository...');
    await execAsync('git init');
    await execAsync('git add .');
    await execAsync('git commit -m "Initial commit: Brotherhood Empire Bot"');
    console.log('✅ Git repository initialized');
  }
}

async function verifyEnvironment() {
  console.log('\n🔍 Verifying environment...');
  
  const requiredFiles = [
    'netlify/functions/telegram-webhook/index.js',
    'netlify/functions/telegram-webhook/package.json',
    'netlify.toml'
  ];
  
  for (const file of requiredFiles) {
    try {
      await fs.access(file);
      console.log(`✅ Found ${file}`);
    } catch {
      throw new Error(`Required file ${file} not found`);
    }
  }
}

async function setup() {
  try {
    console.log('🏰 Brotherhood Empire Bot Setup\n');
    
    // Step 1: Check dependencies
    await checkDependencies();
    
    // Step 2: Verify environment
    await verifyEnvironment();
    
    // Step 3: Setup Git
    await setupGit();
    
    // Step 4: Setup webhook
    const webhookInfo = await setupWebhook();
    
    console.log('\n🎉 Setup completed successfully!\n');
    console.log('Next steps:');
    console.log('\n1. Deploy to Netlify:');
    console.log('   - Create a new site on Netlify');
    console.log('   - Connect this repository');
    console.log('   - Set the following build settings:');
    console.log('     Build command: npm install');
    console.log('     Publish directory: public');
    console.log('     Functions directory: netlify/functions');
    
    console.log('\n2. Add these environment variables in Netlify:');
    console.log('   TELEGRAM_BOT_TOKEN=[Secured]');
    console.log('   GHL_API_KEY=your_ghl_api_key');
    console.log('   MAKE_WEBHOOK_URL=your_make_webhook_url');
    
    console.log('\n3. Test the bot:');
    console.log('   1. Open Telegram');
    console.log('   2. Search for @Brotherhoodempirebot');
    console.log('   3. Send /start command\n');

  } catch (error) {
    console.error('\n❌ Error during setup:', error.message);
    if (error.response?.data) {
      console.error('API Response:', JSON.stringify(error.response.data, null, 2));
    }
    process.exit(1);
  }
}

setup();
