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
Webhook URL: https://ghl-automation-ai.netlify.app/.netlify/functions/telegram-webhook

Initializing git repository...

🎉 Setup completed! Next steps:

1. Verify your Netlify deployment settings:
   Site ID: 4129ca4d-69a4-4d42-96cf-a77169ba3a35
   Site URL: https://ghl-automation-ai.netlify.app

2. Add these environment variables in Netlify:
   TELEGRAM_BOT_TOKEN=7838814763:AAGVkweVaww77zuWb6lUz4Fg6Xm5yiiEido
   GHL_API_KEY=your_ghl_api_key
   MAKE_WEBHOOK_URL=your_make_webhook_url

3. Test the bot:
   1. Open Telegram
   2. Search for @Brotherhoodempirebot
   3. Send /start command
                <path fill="#007067" d="M11.9998836,4.09370803 L8.55809517,7.43294953 C8.23531459,7.74611298 8.23531459,8.25388736 8.55809517,8.56693769 L12,11.9062921 L9.84187871,14 L4.24208544,8.56693751 C3.91930485,8.25388719 3.91930485,7.74611281 4.24208544,7.43294936 L9.84199531,2 L11.9998836,4.09370803 Z"/>
              </svg>
              Back to our site
             </a>
          </p>
          <hr><p>If this is your site, and you weren't expecting a 404 for this path, please visit Netlify's <a href="https://answers.netlify.com/t/support-guide-i-ve-deployed-my-site-but-i-still-see-page-not-found/125?utm_source=404page&utm_campaign=community_tracking">"page not found" support guide</a> for troubleshooting tips.
          </p>
        </div>
      </div>
    </div>
    <script>
      (function() {
        if (document.referrer && document.location.host && document.referrer.match(new RegExp("^https?://" + document.location.host))) {
          document.getElementById("back-link").setAttribute("href", document.referrer);
        }
      })();
    </script>
  </body>
</html>
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100  3082    0  3082    0     0  16704      0 --:--:-- --:--:-- --:--:-- 16841

added 169 packages, and audited 170 packages in 6s

67 packages are looking for funding
  run `npm fund` for details

5 moderate severity vulnerabilities

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
npm warn deprecated har-validator@5.1.5: this library is no longer supported
npm warn deprecated uuid@3.4.0: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.
npm warn deprecated request@2.88.2: request has been deprecated, see https://github.com/request/request/issues/3142
Setting webhook URL to: https://ghl-automation-ai.netlify.app/.netlify/functions/telegram-webhook
Webhook set response: { ok: true, result: true, description: 'Webhook is already set' }

Webhook info: {
  ok: true,
  result: {
    url: 'https://ghl-automation-ai.netlify.app/.netlify/functions/telegram-webhook',
    has_custom_certificate: false,
    pending_update_count: 0,
    max_connections: 40,
    ip_address: '3.125.36.175'
  }
}
{"ok":true,"result":{"url":"https://ghl-automation-ai.netlify.app/.netlify/functions/telegram-webhook","has_custom_certificate":false,"pending_update_count":2,"last_error_date":1733601995,"last_error_message":"Wrong response from the webhook: 404 Not Found","max_connections":40,"ip_address":"3.125.36.175"}}
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100   308  100   308    0     0    825      0 --:--:-- --:--:-- --:--:--   830
Setting webhook URL to: https://ghl-automation-ai.netlify.app/.netlify/functions/telegram-webhook
Webhook deleted: { ok: true, result: true, description: 'Webhook was deleted' }
Webhook set response: { ok: true, result: true, description: 'Webhook was set' }

Webhook info: {
  ok: true,
  result: {
    url: 'https://ghl-automation-ai.netlify.app/.netlify/functions/telegram-webhook',
    has_custom_certificate: false,
    pending_update_count: 0,
    max_connections: 40,
    ip_address: '3.125.36.175'
  }
}
Error: {
  ok: false,
  error_code: 400,
  description: 'Bad Request: chat not found'
}
  }
}

setup();
