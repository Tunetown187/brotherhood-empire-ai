const technicalIndicators = require('technicalindicators');
const axios = require('axios');
const winston = require('winston');

class MarketAnalyzer {
    constructor() {
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            ),
            transports: [
                new winston.transports.File({ filename: 'market_analysis.log' })
            ]
        });
    }

    // Advanced Technical Analysis
    async analyzeTechnicals(priceData) {
        const closes = priceData.map(p => p.close);
        const highs = priceData.map(p => p.high);
        const lows = priceData.map(p => p.low);
        const volumes = priceData.map(p => p.volume);

        return {
            // Trend Indicators
            ema: this.calculateEMA(closes),
            macd: this.calculateMACD(closes),
            adx: this.calculateADX(highs, lows, closes),
            
            // Momentum Indicators
            rsi: this.calculateRSI(closes),
            stochastic: this.calculateStochastic(highs, lows, closes),
            cci: this.calculateCCI(highs, lows, closes),
            
            // Volume Indicators
            obv: this.calculateOBV(closes, volumes),
            mfi: this.calculateMFI(highs, lows, closes, volumes),
            
            // Volatility Indicators
            bollinger: this.calculateBollingerBands(closes),
            atr: this.calculateATR(highs, lows, closes),
            
            // Support/Resistance
            pivotPoints: this.calculatePivotPoints(highs, lows, closes),
            fibonacci: this.calculateFibonacciLevels(highs, lows)
        };
    }

    calculateEMA(values, period = 14) {
        return technicalIndicators.EMA.calculate({
            values: values,
            period: period
        });
    }

    calculateMACD(values) {
        return technicalIndicators.MACD.calculate({
            values: values,
            fastPeriod: 12,
            slowPeriod: 26,
            signalPeriod: 9
        });
    }

    calculateADX(highs, lows, closes, period = 14) {
        return technicalIndicators.ADX.calculate({
            high: highs,
            low: lows,
            close: closes,
            period: period
        });
    }

    calculateRSI(values, period = 14) {
        return technicalIndicators.RSI.calculate({
            values: values,
            period: period
        });
    }

    calculateStochastic(highs, lows, closes, period = 14, signalPeriod = 3) {
        return technicalIndicators.Stochastic.calculate({
            high: highs,
            low: lows,
            close: closes,
            period: period,
            signalPeriod: signalPeriod
        });
    }

    calculateCCI(highs, lows, closes, period = 20) {
        return technicalIndicators.CCI.calculate({
            high: highs,
            low: lows,
            close: closes,
            period: period
        });
    }

    calculateOBV(closes, volumes) {
        return technicalIndicators.OBV.calculate({
            close: closes,
            volume: volumes
        });
    }

    calculateMFI(highs, lows, closes, volumes, period = 14) {
        return technicalIndicators.MFI.calculate({
            high: highs,
            low: lows,
            close: closes,
            volume: volumes,
            period: period
        });
    }

    calculateBollingerBands(values, period = 20, stdDev = 2) {
        return technicalIndicators.BollingerBands.calculate({
            values: values,
            period: period,
            stdDev: stdDev
        });
    }

    calculateATR(highs, lows, closes, period = 14) {
        return technicalIndicators.ATR.calculate({
            high: highs,
            low: lows,
            close: closes,
            period: period
        });
    }

    calculatePivotPoints(highs, lows, closes) {
        const high = highs[highs.length - 1];
        const low = lows[lows.length - 1];
        const close = closes[closes.length - 1];
        
        const pp = (high + low + close) / 3;
        
        return {
            pp: pp,
            r1: 2 * pp - low,
            s1: 2 * pp - high,
            r2: pp + (high - low),
            s2: pp - (high - low),
            r3: high + 2 * (pp - low),
            s3: low - 2 * (high - pp)
        };
    }

    calculateFibonacciLevels(highs, lows) {
        const high = Math.max(...highs);
        const low = Math.min(...lows);
        const diff = high - low;
        
        return {
            level0: high,
            level236: high - diff * 0.236,
            level382: high - diff * 0.382,
            level500: high - diff * 0.5,
            level618: high - diff * 0.618,
            level786: high - diff * 0.786,
            level1000: low
        };
    }

    // Market Sentiment Analysis
    async analyzeSentiment() {
        try {
            // This would integrate with news APIs and social media
            // Implement proper API calls with your keys
            return {
                overallSentiment: 'neutral',
                confidence: 0.5,
                sources: []
            };
        } catch (error) {
            this.logger.error('Sentiment analysis error:', error);
            throw error;
        }
    }

    // Volume Profile Analysis
    analyzeVolumeProfile(priceData) {
        const volumeByPrice = new Map();
        
        priceData.forEach(candle => {
            const priceLevel = Math.round(candle.close);
            const currentVolume = volumeByPrice.get(priceLevel) || 0;
            volumeByPrice.set(priceLevel, currentVolume + candle.volume);
        });
        
        return {
            volumeByPrice: Object.fromEntries(volumeByPrice),
            poc: this.findPriceOfControl(volumeByPrice),
            valueArea: this.calculateValueArea(volumeByPrice)
        };
    }

    findPriceOfControl(volumeByPrice) {
        let maxVolume = 0;
        let poc = 0;
        
        for (const [price, volume] of volumeByPrice.entries()) {
            if (volume > maxVolume) {
                maxVolume = volume;
                poc = price;
            }
        }
        
        return poc;
    }

    calculateValueArea(volumeByPrice, valueAreaPercent = 0.68) {
        const totalVolume = Array.from(volumeByPrice.values()).reduce((a, b) => a + b, 0);
        const targetVolume = totalVolume * valueAreaPercent;
        
        let currentVolume = 0;
        let upperPrice = this.findPriceOfControl(volumeByPrice);
        let lowerPrice = upperPrice;
        
        while (currentVolume < targetVolume) {
            const upperVolume = volumeByPrice.get(upperPrice + 1) || 0;
            const lowerVolume = volumeByPrice.get(lowerPrice - 1) || 0;
            
            if (upperVolume > lowerVolume) {
                upperPrice++;
                currentVolume += upperVolume;
            } else {
                lowerPrice--;
                currentVolume += lowerVolume;
            }
        }
        
        return { upper: upperPrice, lower: lowerPrice };
    }
}

module.exports = MarketAnalyzer;
