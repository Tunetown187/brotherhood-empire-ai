const winston = require('winston');
const technicalIndicators = require('technicalindicators');

class Backtester {
    constructor(strategy, riskManager) {
        this.strategy = strategy;
        this.riskManager = riskManager;
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            ),
            transports: [
                new winston.transports.File({ filename: 'backtest.log' })
            ]
        });
    }

    async runBacktest(historicalData, initialCapital = 10000) {
        const results = {
            trades: [],
            equity: [initialCapital],
            positions: [],
            metrics: {}
        };

        let capital = initialCapital;
        let position = null;

        for (let i = 100; i < historicalData.length; i++) {
            const slice = historicalData.slice(0, i + 1);
            const signal = await this.strategy.analyze(slice);

            if (signal.signal === 'buy' && !position) {
                const size = this.riskManager.calculatePositionSize(
                    capital,
                    historicalData[i].close
                );

                position = {
                    type: 'long',
                    entry: historicalData[i].close,
                    size: size,
                    entryTime: historicalData[i].timestamp
                };

                results.trades.push({
                    type: 'entry',
                    position: 'long',
                    price: position.entry,
                    size: position.size,
                    time: position.entryTime
                });

            } else if (signal.signal === 'sell' && position) {
                const exit = historicalData[i].close;
                const profit = (exit - position.entry) * position.size;
                capital += profit;

                results.trades.push({
                    type: 'exit',
                    position: 'long',
                    price: exit,
                    size: position.size,
                    profit: profit,
                    time: historicalData[i].timestamp
                });

                position = null;
            }

            results.equity.push(capital + (position ? 
                (historicalData[i].close - position.entry) * position.size : 0));
            
            if (position) {
                results.positions.push({
                    time: historicalData[i].timestamp,
                    price: historicalData[i].close,
                    profit: (historicalData[i].close - position.entry) * position.size
                });
            }
        }

        results.metrics = this.calculateMetrics(results);
        return results;
    }

    calculateMetrics(results) {
        const trades = results.trades.filter(t => t.type === 'exit');
        const profits = trades.map(t => t.profit);
        const equity = results.equity;

        const metrics = {
            totalTrades: trades.length,
            profitableTrades: profits.filter(p => p > 0).length,
            totalProfit: profits.reduce((a, b) => a + b, 0),
            winRate: profits.filter(p => p > 0).length / trades.length,
            maxDrawdown: this.calculateMaxDrawdown(equity),
            sharpeRatio: this.calculateSharpeRatio(equity),
            averageProfit: profits.reduce((a, b) => a + b, 0) / trades.length,
            profitFactor: this.calculateProfitFactor(profits)
        };

        return metrics;
    }

    calculateMaxDrawdown(equity) {
        let maxDrawdown = 0;
        let peak = equity[0];

        for (const value of equity) {
            if (value > peak) {
                peak = value;
            }
            const drawdown = (peak - value) / peak;
            if (drawdown > maxDrawdown) {
                maxDrawdown = drawdown;
            }
        }

        return maxDrawdown;
    }

    calculateSharpeRatio(equity) {
        const returns = [];
        for (let i = 1; i < equity.length; i++) {
            returns.push((equity[i] - equity[i-1]) / equity[i-1]);
        }

        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const stdDev = Math.sqrt(
            returns.reduce((a, b) => a + Math.pow(b - avgReturn, 2), 0) / returns.length
        );

        return avgReturn / stdDev * Math.sqrt(252); // Annualized
    }

    calculateProfitFactor(profits) {
        const gains = profits.filter(p => p > 0).reduce((a, b) => a + b, 0);
        const losses = Math.abs(profits.filter(p => p < 0).reduce((a, b) => a + b, 0));
        return gains / losses;
    }
}

module.exports = Backtester;
