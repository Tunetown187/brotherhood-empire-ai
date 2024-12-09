const ccxt = require('ccxt');
const winston = require('winston');

class ExchangeManager {
    constructor() {
        this.exchanges = new Map();
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            ),
            transports: [
                new winston.transports.File({ filename: 'exchange.log' })
            ]
        });
    }

    async initializeExchange(exchangeId, config = {}) {
        try {
            if (!ccxt[exchangeId]) {
                throw new Error(`Exchange ${exchangeId} not supported`);
            }

            const exchange = new ccxt[exchangeId](config);
            await exchange.loadMarkets();
            
            this.exchanges.set(exchangeId, exchange);
            this.logger.info(`Initialized ${exchangeId} exchange`);
            
            return exchange;
        } catch (error) {
            this.logger.error(`Failed to initialize ${exchangeId}:`, error);
            throw error;
        }
    }

    async getMarkets(exchangeId) {
        const exchange = this.exchanges.get(exchangeId);
        if (!exchange) {
            throw new Error(`Exchange ${exchangeId} not initialized`);
        }
        
        return exchange.markets;
    }

    async getOrderBook(exchangeId, symbol) {
        const exchange = this.exchanges.get(exchangeId);
        if (!exchange) {
            throw new Error(`Exchange ${exchangeId} not initialized`);
        }
        
        return exchange.fetchOrderBook(symbol);
    }

    async getTicker(exchangeId, symbol) {
        const exchange = this.exchanges.get(exchangeId);
        if (!exchange) {
            throw new Error(`Exchange ${exchangeId} not initialized`);
        }
        
        return exchange.fetchTicker(symbol);
    }

    async getBalance(exchangeId) {
        const exchange = this.exchanges.get(exchangeId);
        if (!exchange) {
            throw new Error(`Exchange ${exchangeId} not initialized`);
        }
        
        return exchange.fetchBalance();
    }
}

module.exports = ExchangeManager;
