const ccxt = require('ccxt');
const technicalIndicators = require('technicalindicators');
const winston = require('winston');

class TradingStrategy {
    constructor(exchange, symbol, timeframe = '1m') {
        this.exchange = new ccxt[exchange]();
        this.symbol = symbol;
        this.timeframe = timeframe;
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            ),
            transports: [
                new winston.transports.File({ filename: 'trading.log' })
            ]
        });
    }

    async getMarketData() {
        try {
            const ohlcv = await this.exchange.fetchOHLCV(this.symbol, this.timeframe);
            return ohlcv.map(candle => ({
                timestamp: candle[0],
                open: candle[1],
                high: candle[2],
                low: candle[3],
                close: candle[4],
                volume: candle[5]
            }));
        } catch (error) {
            this.logger.error('Error fetching market data:', error);
            throw error;
        }
    }

    calculateRSI(closes, period = 14) {
        return technicalIndicators.RSI.calculate({
            values: closes,
            period: period
        });
    }

    calculateMACD(closes) {
        return technicalIndicators.MACD.calculate({
            values: closes,
            fastPeriod: 12,
            slowPeriod: 26,
            signalPeriod: 9
        });
    }

    async backtest(startTime, endTime) {
        try {
            const marketData = await this.getMarketData();
            const results = {
                trades: [],
                totalProfit: 0,
                winRate: 0,
                maxDrawdown: 0
            };
            
            // Implement backtesting logic here
            
            return results;
        } catch (error) {
            this.logger.error('Backtesting error:', error);
            throw error;
        }
    }
}

class MACrossStrategy extends TradingStrategy {
    constructor(exchange, symbol, fastPeriod = 10, slowPeriod = 20) {
        super(exchange, symbol);
        this.fastPeriod = fastPeriod;
        this.slowPeriod = slowPeriod;
    }

    async analyze() {
        const data = await this.getMarketData();
        const closes = data.map(candle => candle.close);
        
        const fastMA = technicalIndicators.SMA.calculate({
            values: closes,
            period: this.fastPeriod
        });
        
        const slowMA = technicalIndicators.SMA.calculate({
            values: closes,
            period: this.slowPeriod
        });

        const lastFastMA = fastMA[fastMA.length - 1];
        const lastSlowMA = slowMA[slowMA.length - 1];
        
        return {
            signal: lastFastMA > lastSlowMA ? 'buy' : 'sell',
            fastMA: lastFastMA,
            slowMA: lastSlowMA,
            currentPrice: closes[closes.length - 1]
        };
    }
}

class RSIMACDStrategy extends TradingStrategy {
    constructor(exchange, symbol) {
        super(exchange, symbol);
    }

    async analyze() {
        const data = await this.getMarketData();
        const closes = data.map(candle => candle.close);
        
        const rsi = this.calculateRSI(closes);
        const macd = this.calculateMACD(closes);
        
        const lastRSI = rsi[rsi.length - 1];
        const lastMACD = macd[macd.length - 1];

        let signal = 'hold';
        if (lastRSI < 30 && lastMACD.histogram > 0) {
            signal = 'buy';
        } else if (lastRSI > 70 && lastMACD.histogram < 0) {
            signal = 'sell';
        }

        return {
            signal,
            rsi: lastRSI,
            macd: lastMACD,
            currentPrice: closes[closes.length - 1]
        };
    }
}

module.exports = {
    TradingStrategy,
    MACrossStrategy,
    RSIMACDStrategy
};
