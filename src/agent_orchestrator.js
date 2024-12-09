const { CommunicationAgent, SalesAgent, MarketingAgent, OperationsAgent, WebDevAgent, SEOAgent, BusinessAgent } = require('../empire_core/ai_agents');
const { PAYMENT_CONFIG } = require('../setup');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const Web3 = require('web3');

class AgentOrchestrator {
    constructor() {
        this.agents = {
            communication: new CommunicationAgent(),
            sales: new SalesAgent(),
            marketing: new MarketingAgent(),
            operations: new OperationsAgent(),
            webdev: new WebDevAgent(),
            seo: new SEOAgent(),
            business: new BusinessAgent()
        };
        
        this.web3 = new Web3();
        this.initializePaymentProcessors();
    }

    async initializePaymentProcessors() {
        // Initialize Stripe
        this.stripe = stripe;

        // Initialize crypto if enabled
        if (PAYMENT_CONFIG.cryptoEnabled) {
            this.cryptoWallet = PAYMENT_CONFIG.cryptoWallet;
        }
    }

    async startContinuousOperation() {
        console.log('🚀 Starting Brotherhood Empire AI Agents...');
        
        // Start all agents in parallel
        await Promise.all([
            this.runCommunicationAgent(),
            this.runSalesAgent(),
            this.runMarketingAgent(),
            this.runOperationsAgent(),
            this.runWebDevAgent(),
            this.runSEOAgent(),
            this.runBusinessAgent()
        ]);
    }

    async runCommunicationAgent() {
        while (true) {
            try {
                await this.agents.communication.handleConversations();
                await this.agents.communication.manageDripCampaigns();
                await new Promise(resolve => setTimeout(resolve, 5000)); // 5-second interval
            } catch (error) {
                console.error('Communication Agent Error:', error);
            }
        }
    }

    async runSalesAgent() {
        while (true) {
            try {
                await this.agents.sales.processLeads();
                await this.agents.sales.negotiateDeals();
                await this.handlePayments();
                await new Promise(resolve => setTimeout(resolve, 10000)); // 10-second interval
            } catch (error) {
                console.error('Sales Agent Error:', error);
            }
        }
    }

    async runMarketingAgent() {
        while (true) {
            try {
                await this.agents.marketing.optimizeCampaigns();
                await this.agents.marketing.analyzeMetrics();
                await new Promise(resolve => setTimeout(resolve, 15000)); // 15-second interval
            } catch (error) {
                console.error('Marketing Agent Error:', error);
            }
        }
    }

    async runOperationsAgent() {
        while (true) {
            try {
                await this.agents.operations.optimizeWorkflows();
                await this.agents.operations.monitorPerformance();
                await new Promise(resolve => setTimeout(resolve, 20000)); // 20-second interval
            } catch (error) {
                console.error('Operations Agent Error:', error);
            }
        }
    }

    async runWebDevAgent() {
        while (true) {
            try {
                await this.agents.webdev.optimizeWebsites();
                await this.agents.webdev.trackConversions();
                await new Promise(resolve => setTimeout(resolve, 30000)); // 30-second interval
            } catch (error) {
                console.error('WebDev Agent Error:', error);
            }
        }
    }

    async runSEOAgent() {
        while (true) {
            try {
                await this.agents.seo.optimizeContent();
                await this.agents.seo.analyzeBacklinks();
                await new Promise(resolve => setTimeout(resolve, 60000)); // 1-minute interval
            } catch (error) {
                console.error('SEO Agent Error:', error);
            }
        }
    }

    async runBusinessAgent() {
        while (true) {
            try {
                await this.agents.business.analyzeMarket();
                await this.agents.business.optimizeStrategy();
                await new Promise(resolve => setTimeout(resolve, 300000)); // 5-minute interval
            } catch (error) {
                console.error('Business Agent Error:', error);
            }
        }
    }

    async handlePayments() {
        try {
            // Process Stripe payments
            const pendingPayments = await this.stripe.paymentIntents.list({
                limit: 100,
                status: 'requires_capture'
            });

            for (const payment of pendingPayments.data) {
                await this.stripe.paymentIntents.capture(payment.id);
                console.log(`💰 Payment captured: ${payment.amount / 100} ${payment.currency.toUpperCase()}`);
            }

            // Handle crypto payments if enabled
            if (PAYMENT_CONFIG.cryptoEnabled) {
                const balance = await this.web3.eth.getBalance(this.cryptoWallet);
                console.log(`💎 Crypto wallet balance: ${this.web3.utils.fromWei(balance, 'ether')} ETH`);
            }

        } catch (error) {
            console.error('Payment Processing Error:', error);
        }
    }
}

module.exports = AgentOrchestrator;
