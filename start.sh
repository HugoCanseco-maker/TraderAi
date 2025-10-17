#!/bin/bash

# TraderBlockAI Startup Script
echo "🚀 Starting TraderBlockAI MVP..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm and try again."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Start backend in background
echo "🐍 Starting Python backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "⚛️  Starting Next.js frontend..."
cd traderblockai-app
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 TraderBlockAI is starting up!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 Frontend App: http://localhost:3000"
echo ""
echo "📚 Educational Features:"
echo "   • AI-powered stock analysis"
echo "   • Interactive charts with forecasts"
echo "   • Educational tooltips and explanations"
echo "   • Prominent legal disclaimers"
echo ""
echo "⚠️  IMPORTANT: This is for educational purposes only. Not financial advice."
echo ""
echo "Press Ctrl+C to stop both services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping TraderBlockAI..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Stopped successfully"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for user to stop
wait
