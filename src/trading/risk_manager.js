const winston = require('winston');

class RiskManager {
    constructor(config = {}) {
        this.maxPositionSize = config.maxPositionSize || 0.1; // 10% of portfolio
        this.stopLossPercent = config.stopLossPercent || 0.02; // 2% loss per trade
        this.maxDrawdownPercent = config.maxDrawdownPercent || 0.1; // 10% max drawdown
        this.maxLeverage = config.maxLeverage || 1; // No leverage by default
        
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            ),
            transports: [
                new winston.transports.File({ filename: 'risk.log' })
            ]
        });
    }

    calculatePositionSize(portfolioValue, currentPrice, riskPerTrade = 0.01) {
        const maxPositionValue = portfolioValue * this.maxPositionSize;
        const riskAmount = portfolioValue * riskPerTrade;
        const stopLossDistance = currentPrice * this.stopLossPercent;
        
        let positionSize = riskAmount / stopLossDistance;
        const positionValue = positionSize * currentPrice;
        
        if (positionValue > maxPositionValue) {
            positionSize = maxPositionValue / currentPrice;
        }
        
        return Math.floor(positionSize * 100000) / 100000; // Round to 5 decimals
    }

    validateTrade(trade) {
        const validations = {
            positionSize: this.validatePositionSize(trade),
            stopLoss: this.validateStopLoss(trade),
            leverage: this.validateLeverage(trade),
            risk: this.calculateRiskRewardRatio(trade)
        };
        
        return {
            valid: Object.values(validations).every(v => v.valid),
            validations
        };
    }

    validatePositionSize(trade) {
        const positionValue = trade.size * trade.price;
        const maxValue = trade.portfolioValue * this.maxPositionSize;
        
        return {
            valid: positionValue <= maxValue,
            message: positionValue <= maxValue ? 
                'Position size within limits' : 
                'Position size exceeds maximum allowed'
        };
    }

    validateStopLoss(trade) {
        if (!trade.stopLoss) {
            return {
                valid: false,
                message: 'Stop loss not set'
            };
        }
        
        const stopLossPercent = Math.abs(trade.price - trade.stopLoss) / trade.price;
        
        return {
            valid: stopLossPercent <= this.stopLossPercent,
            message: stopLossPercent <= this.stopLossPercent ?
                'Stop loss within limits' :
                'Stop loss exceeds maximum allowed'
        };
    }

    validateLeverage(trade) {
        return {
            valid: trade.leverage <= this.maxLeverage,
            message: trade.leverage <= this.maxLeverage ?
                'Leverage within limits' :
                'Leverage exceeds maximum allowed'
        };
    }

    calculateRiskRewardRatio(trade) {
        if (!trade.takeProfit || !trade.stopLoss) {
            return {
                valid: false,
                message: 'Take profit or stop loss not set'
            };
        }
        
        const risk = Math.abs(trade.price - trade.stopLoss);
        const reward = Math.abs(trade.takeProfit - trade.price);
        const ratio = reward / risk;
        
        return {
            valid: ratio >= 2,
            message: ratio >= 2 ?
                `Risk-reward ratio acceptable (${ratio.toFixed(2)})` :
                `Risk-reward ratio too low (${ratio.toFixed(2)})`
        };
    }

    async monitorDrawdown(portfolioHistory) {
        const initialValue = portfolioHistory[0];
        const currentValue = portfolioHistory[portfolioHistory.length - 1];
        const maxValue = Math.max(...portfolioHistory);
        
        const drawdown = (maxValue - currentValue) / maxValue;
        
        if (drawdown > this.maxDrawdownPercent) {
            this.logger.warn(`Maximum drawdown exceeded: ${(drawdown * 100).toFixed(2)}%`);
            return {
                exceeded: true,
                drawdown,
                message: 'Maximum drawdown exceeded'
            };
        }
        
        return {
            exceeded: false,
            drawdown,
            message: 'Drawdown within limits'
        };
    }
}

module.exports = RiskManager;
