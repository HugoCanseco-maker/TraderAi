# TraderBlockAI MVP

An AI-powered stock analysis dashboard that educates novice investors by blending predictive AI forecasts with traditional financial analysis, while clearly disclaiming its nature as an educational tool.

## 🚨 Important Legal Notice

**This is a technology demonstration using statistical modeling and is for educational purposes only. This is not financial advice. All investment decisions should be made with the help of a qualified financial professional.**

## 🏗️ Architecture

### Frontend (Next.js + React)
- **Framework**: Next.js 14 with App Router
- **UI Library**: shadcn/ui components with Tailwind CSS
- **Charts**: Recharts for interactive stock charts
- **Deployment**: Vercel

### Backend (Python + FastAPI)
- **Framework**: FastAPI
- **AI Model**: LSTM neural network for price forecasting
- **Data Source**: Yahoo Finance API (yfinance)
- **Technical Analysis**: Custom implementation of SMA, RSI, MACD
- **Deployment**: Render

## 🎯 Features

### Core Functionality
1. **Interactive Stock Chart**: Historical data with SMAs and AI forecast
2. **AI Analysis Panel**: Trend, momentum, and volatility analysis with educational tooltips
3. **Learning Corner**: Narrative explanations of technical indicators
4. **Legal Disclaimer**: Prominent, non-dismissible disclaimer banner

### Educational Components
- Tooltip explanations for each metric (Trend, Momentum, Volatility)
- Comprehensive technical indicator analysis
- User-friendly explanations of complex financial concepts
- Clear disclaimers about educational purpose

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TraderAi
   ```

2. **Start the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
   Backend will be available at `http://localhost:8000`

3. **Start the frontend** (in a new terminal)
   ```bash
   cd traderblockai-app
   npm install
   npm run dev
   ```
   Frontend will be available at `http://localhost:3000`

### Using Docker

```bash
docker-compose up --build
```

## 📁 Project Structure

```
TraderAi/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container config
├── traderblockai-app/
│   ├── app/
│   │   ├── components/
│   │   │   ├── ui/         # shadcn/ui components
│   │   │   ├── AnalysisDashboard.tsx
│   │   │   ├── Disclaimer.tsx      # Legal disclaimer
│   │   │   ├── StockChart.tsx
│   │   │   └── TickerInput.tsx
│   │   ├── layout.tsx
│   │   └── page.tsx        # Main application page
│   ├── lib/
│   │   └── utils.ts        # Utility functions
│   ├── package.json
│   └── Dockerfile         # Frontend container config
└── docker-compose.yml     # Full stack deployment
```

## 🔧 Configuration

### Environment Variables

**Backend** (required for production):
- `FRONTEND_URL`: Your deployed frontend URL (e.g., https://your-app.vercel.app)
- Used for secure CORS configuration

**Frontend** (optional):
- `NEXT_PUBLIC_API_URL`: Backend API URL (defaults to https://traderai-r9iz.onrender.com)

### API Endpoints

- `GET /api/v1/analyze/{ticker}`: Analyze a stock ticker
- `GET /`: Health check endpoint

## 🚀 Deployment

### Backend to Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Configure:
   - **Environment**: `Docker` (Crucial: This tells Render to use our Dockerfile)
   - **Root Directory**: `backend` (This is the critical fix for the error)
   - **Build Command**: (Render will automatically use your Dockerfile)
   - **Start Command**: (Render will automatically use your Dockerfile)

### Frontend to Vercel

1. Connect your GitHub repository to Vercel
2. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `traderblockai-app`
   - **Environment Variables**: `NEXT_PUBLIC_API_URL` = your Render backend URL

## 🧪 Testing

### Backend API Testing
```bash
curl http://localhost:8000/api/v1/analyze/AAPL
```

### Frontend Testing
The application includes mock data for demonstration. To test with real API:

1. Deploy backend to Render
2. Update `NEXT_PUBLIC_API_URL` in frontend environment
3. Uncomment the real API call in `page.tsx`

## 📊 Sample Analysis Response

```json
{
  "ticker": "AAPL",
  "current_price": 150.25,
  "trend": "Bullish",
  "momentum": "Positive", 
  "volatility": "Medium",
  "confidence": 0.82,
  "forecast": {
    "day_1": 152.30,
    "day_2": 154.15,
    "day_3": 155.80
  },
  "sma_20": 148.50,
  "sma_50": 145.75,
  "rsi": 65.2,
  "macd": 1.25,
  "educational_explanation": "The stock AAPL shows a bullish trend..."
}
```

## 🛡️ Legal Compliance

This application includes:
- **Prominent Legal Disclaimer**: Always visible at the bottom of the interface
- **Educational Focus**: All content emphasizes learning over investment advice
- **Clear Disclaimers**: Multiple warnings about not being financial advice
- **Professional Guidance**: Encouragement to consult qualified professionals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all legal disclaimers remain prominent
5. Submit a pull request

## 📄 License

This project is for educational purposes only. See LICENSE file for details.

## ⚠️ Disclaimer

**This application is for educational purposes only and should not be considered as financial advice. All investment decisions should be made with the help of a qualified financial professional.**
