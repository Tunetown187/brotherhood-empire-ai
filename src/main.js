const express = require('express');
const AgentOrchestrator = require('./agent_orchestrator');
const { PAYMENT_CONFIG, GHL_CONFIG, initGHLPayments } = require('../setup');

const app = express();
const port = process.env.PORT || 3000;

// Initialize the agent orchestrator
const orchestrator = new AgentOrchestrator();
let ghlClient;

app.use(express.json());

// Initialize GHL payments
initGHLPayments()
    .then(client => {
        ghlClient = client;
        console.log('💳 GoHighLevel payment system initialized');
    })
    .catch(error => console.error('Failed to initialize GHL payments:', error));

// Start the continuous operation of AI agents
orchestrator.startContinuousOperation()
    .catch(error => console.error('Error starting agents:', error));

// API endpoints for monitoring and control
app.get('/status', (req, res) => {
    res.json({
        status: 'running',
        agents: Object.keys(orchestrator.agents),
        paymentConfig: {
            ghlEnabled: !!GHL_CONFIG.apiKey,
            cryptoEnabled: PAYMENT_CONFIG.cryptoEnabled,
            packages: PAYMENT_CONFIG.packages
        }
    });
});

// Endpoint to create a payment through GoHighLevel
app.post('/create-payment', async (req, res) => {
    try {
        const { package, paymentMethod, customerInfo } = req.body;
        
        if (!PAYMENT_CONFIG.packages[package]) {
            return res.status(400).json({ error: 'Invalid package selected' });
        }

        const selectedPackage = PAYMENT_CONFIG.packages[package];

        if (paymentMethod === 'ghl') {
            // Create order in GoHighLevel
            const orderData = {
                locationId: GHL_CONFIG.location,
                productId: selectedPackage.ghlProductId,
                amount: selectedPackage.price,
                currency: 'USD',
                customer: customerInfo
            };

            const response = await ghlClient.post('orders/', orderData);
            
            res.json({
                orderId: response.data.orderId,
                paymentUrl: response.data.paymentUrl,
                amount: selectedPackage.price
            });
        } else if (paymentMethod === 'crypto') {
            res.json({
                wallet: PAYMENT_CONFIG.cryptoWallet,
                amount: selectedPackage.price,
                message: 'Please send the exact amount to the provided wallet address'
            });
        } else {
            res.status(400).json({ error: 'Invalid payment method' });
        }
    } catch (error) {
        console.error('Payment creation error:', error);
        res.status(500).json({ error: 'Failed to create payment' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`🚀 Brotherhood Empire server running on port ${port}`);
    console.log('💼 AI Agents operating 24/7 for maximum profit');
    console.log('💰 Payment systems initialized with GoHighLevel integration');
});
