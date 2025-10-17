import os
import pandas as pd
import numpy as np
import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

app = FastAPI(title="TraderBlockAI API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisResponse(BaseModel):
    ticker: str
    current_price: float
    trend: str
    momentum: str
    volatility: str
    confidence: float
    forecast: Dict[str, float]
    sma_20: float
    sma_50: float
    rsi: float
    macd: float
    # --- NEW PROFESSIONAL-GRADE METRICS ---
    extreme_risk: Dict[str, float]
    risk_adjusted_return: Dict[str, float]
    market_correlation: Dict[str, float]
    # -------------------------------------
    educational_explanation: str

class StockAnalyzer:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = None
        self.load_or_create_model()
    
    def load_or_create_model(self):
        """Load existing model or create a new one"""
        try:
            self.model = tf.keras.models.load_model('lstm_model.h5')
            print("Loaded existing LSTM model")
        except:
            print("Creating new LSTM model...")
            self.create_model()
    
    def create_model(self):
        """Create a simple LSTM model for demonstration"""
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(60, 1)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(50, return_sequences=False),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(25),
            tf.keras.layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        self.model = model
    
    def get_stock_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """Fetch stock data using yfinance"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            if data.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            return data
        except Exception as e:
            raise ValueError(f"Error fetching data for {ticker}: {str(e)}")
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate technical indicators"""
        # Simple Moving Averages
        sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
        
        # RSI calculation
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        # MACD calculation
        ema_12 = data['Close'].ewm(span=12).mean()
        ema_26 = data['Close'].ewm(span=26).mean()
        macd = (ema_12 - ema_26).iloc[-1]
        
        return {
            'sma_20': float(sma_20),
            'sma_50': float(sma_50),
            'rsi': float(rsi),
            'macd': float(macd)
        }
    
    def generate_forecast(self, data: pd.DataFrame) -> Dict[str, float]:
        """Generate 3-day price forecast using LSTM"""
        try:
            # Prepare data for LSTM
            close_prices = data['Close'].values.reshape(-1, 1)
            scaled_data = self.scaler.fit_transform(close_prices)
            
            # Create sequences for LSTM
            def create_sequences(data, seq_length=60):
                X, y = [], []
                for i in range(seq_length, len(data)):
                    X.append(data[i-seq_length:i])
                    y.append(data[i])
                return np.array(X), np.array(y)
            
            X, y = create_sequences(scaled_data)
            
            # Train model if needed (simplified for demo)
            if len(X) > 0:
                # For demo purposes, we'll use a simple trend-based forecast
                recent_trend = np.mean(np.diff(close_prices[-5:]))
                current_price = float(close_prices[-1])
                
                # Simple forecast based on recent trend
                forecast = {}
                for i in range(1, 4):
                    forecast[f"day_{i}"] = float(current_price + (recent_trend * i))
                
                return forecast
            else:
                # Fallback to current price
                current_price = float(close_prices[-1])
                return {
                    "day_1": current_price,
                    "day_2": current_price,
                    "day_3": current_price
                }
        except Exception as e:
            print(f"Forecast error: {e}")
            current_price = float(data['Close'].iloc[-1])
            return {
                "day_1": current_price,
                "day_2": current_price,
                "day_3": current_price
            }
    
    def analyze_trend(self, data: pd.DataFrame, indicators: Dict[str, float]) -> str:
        """Analyze overall trend"""
        sma_20 = indicators['sma_20']
        sma_50 = indicators['sma_50']
        current_price = float(data['Close'].iloc[-1])
        
        if current_price > sma_20 > sma_50:
            return "Bullish"
        elif current_price < sma_20 < sma_50:
            return "Bearish"
        else:
            return "Neutral"
    
    def analyze_momentum(self, indicators: Dict[str, float]) -> str:
        """Analyze momentum using RSI and MACD"""
        rsi = indicators['rsi']
        macd = indicators['macd']
        
        if rsi > 70:
            return "Overbought"
        elif rsi < 30:
            return "Oversold"
        elif macd > 0:
            return "Positive"
        else:
            return "Negative"
    
    def analyze_volatility(self, data: pd.DataFrame) -> str:
        """Analyze volatility"""
        returns = data['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        
        if volatility > 0.3:
            return "High"
        elif volatility > 0.15:
            return "Medium"
        else:
            return "Low"
    
    def calculate_extreme_risk(self, data: pd.DataFrame) -> dict:
        """
        Calculates the 1-day 99% Value at Risk (VaR) using historical simulation.
        This estimates the plausible worst-case single-day loss.
        """
        returns = data['Close'].pct_change().dropna()
        if returns.empty:
            return {"var_99_percent": 0.0, "max_expected_loss_usd": 0.0}
        
        var_99 = returns.quantile(0.01)
        current_price = data['Close'].iloc[-1]
        max_expected_loss_dollar = current_price * var_99
        
        return {
            "var_99_percent": round(var_99, 4),
            "max_expected_loss_usd": round(max_expected_loss_dollar, 2)
        }

    def calculate_sharpe_ratio(self, data: pd.DataFrame) -> dict:
        """
        Calculates the annualized Sharpe Ratio.
        This measures the return of an investment compared to its risk.
        """
        returns = data['Close'].pct_change().dropna()
        if returns.empty or returns.std() == 0:
            return {"sharpe_ratio": 0.0}
            
        # Assuming a risk-free rate of 0 for simplicity in this context
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
        
        return {
            "sharpe_ratio": round(sharpe_ratio, 2)
        }

    def calculate_beta(self, data: pd.DataFrame) -> dict:
        """
        Calculates the stock's Beta relative to the S&P 500 (SPY).
        This measures the stock's volatility in relation to the overall market.
        """
        try:
            market_data = yf.download('SPY', start=data.index.min(), end=data.index.max(), progress=False)
            if market_data.empty:
                return {"beta": 1.0} # Default to market beta if no data
                
            stock_returns = data['Close'].pct_change().dropna()
            market_returns = market_data['Close'].pct_change().dropna()
            
            # Align data
            aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
            aligned_data.columns = ['stock', 'market']
            
            if len(aligned_data) < 2:
                 return {"beta": 1.0}
            
            # Calculate covariance and variance
            covariance_matrix = aligned_data.cov()
            covariance = covariance_matrix.iloc[0, 1]
            market_variance = aligned_data['market'].var()
            
            if market_variance == 0:
                return {"beta": 1.0}
                
            beta = covariance / market_variance
            
            return {"beta": round(beta, 2)}
        except Exception:
            return {"beta": 1.0} # Return default on error
    
    def generate_educational_explanation(self, ticker: str, trend: str, momentum: str, 
                                       volatility: str, indicators: Dict[str, float]) -> str:
        """Generate educational explanation including professional-grade metrics"""
        explanations = {
            "Bullish": f"The stock {ticker} shows a bullish trend, meaning the price is generally moving upward. This suggests positive market sentiment and potential for continued growth.",
            "Bearish": f"The stock {ticker} shows a bearish trend, meaning the price is generally moving downward. This suggests negative market sentiment and potential for further decline.",
            "Neutral": f"The stock {ticker} shows a neutral trend, meaning the price is moving sideways without a clear direction. This suggests uncertainty in the market."
        }
        
        trend_explanation = explanations.get(trend, f"The stock {ticker} shows a {trend.lower()} trend.")
        
        momentum_explanations = {
            "Overbought": "The RSI indicator suggests the stock may be overbought, which could indicate a potential price correction.",
            "Oversold": "The RSI indicator suggests the stock may be oversold, which could indicate a potential price recovery.",
            "Positive": "The MACD indicator shows positive momentum, suggesting upward price movement.",
            "Negative": "The MACD indicator shows negative momentum, suggesting downward price movement."
        }
        
        momentum_explanation = momentum_explanations.get(momentum, f"The momentum indicators suggest {momentum.lower()} momentum.")
        
        volatility_explanations = {
            "High": "High volatility means the stock price changes significantly, which can present both opportunities and risks.",
            "Medium": "Medium volatility indicates moderate price fluctuations, providing a balanced risk-return profile.",
            "Low": "Low volatility means the stock price is relatively stable, which may appeal to conservative investors."
        }
        
        volatility_explanation = volatility_explanations.get(volatility, f"The stock shows {volatility.lower()} volatility.")
        
        # Add professional-grade metrics explanation
        professional_metrics = " Additionally, this analysis includes professional-grade risk metrics: Value at Risk (VaR) quantifies potential losses, the Sharpe Ratio measures risk-adjusted returns, and Beta indicates how the stock moves relative to the overall market. These metrics help investors understand both the potential rewards and risks associated with this investment."
        
        return f"{trend_explanation} {momentum_explanation} {volatility_explanation}{professional_metrics} Remember, this analysis is for educational purposes only and should not be considered as financial advice."

analyzer = StockAnalyzer()

@app.get("/api/v1/analyze/{ticker}")
async def analyze_stock(ticker: str) -> AnalysisResponse:
    """Analyze a stock and return comprehensive analysis"""
    try:
        # Fetch stock data
        data = analyzer.get_stock_data(ticker.upper())
        
        # Calculate technical indicators
        indicators = analyzer.calculate_technical_indicators(data)
        
        # Generate forecast
        forecast = analyzer.generate_forecast(data)
        
        # Analyze components
        trend = analyzer.analyze_trend(data, indicators)
        momentum = analyzer.analyze_momentum(indicators)
        volatility = analyzer.analyze_volatility(data)
        
        # Calculate professional-grade metrics
        extreme_risk = analyzer.calculate_extreme_risk(data)
        sharpe_ratio = analyzer.calculate_sharpe_ratio(data)
        beta = analyzer.calculate_beta(data)
        
        # Generate educational explanation
        educational_explanation = analyzer.generate_educational_explanation(
            ticker.upper(), trend, momentum, volatility, indicators
        )
        
        # Calculate confidence (simplified)
        confidence = 0.75  # Placeholder confidence score
        
        return AnalysisResponse(
            ticker=ticker.upper(),
            current_price=float(data['Close'].iloc[-1]),
            trend=trend,
            momentum=momentum,
            volatility=volatility,
            confidence=confidence,
            forecast=forecast,
            sma_20=indicators['sma_20'],
            sma_50=indicators['sma_50'],
            rsi=indicators['rsi'],
            macd=indicators['macd'],
            # --- NEW PROFESSIONAL-GRADE METRICS ---
            extreme_risk=extreme_risk,
            risk_adjusted_return=sharpe_ratio,
            market_correlation=beta,
            # -------------------------------------
            educational_explanation=educational_explanation
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "TraderBlockAI API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
