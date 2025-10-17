'use client'

import React, { useState } from 'react'
import TickerInput from './components/TickerInput'
import StockChart from './components/StockChart'
import AnalysisDashboard from './components/AnalysisDashboard'
import Disclaimer from './components/Disclaimer'

interface AnalysisData {
  ticker: string
  current_price: number
  trend: string
  momentum: string
  volatility: string
  confidence: number
  forecast: { day_1: number; day_2: number; day_3: number }
  sma_20: number
  sma_50: number
  rsi: number
  macd: number
  // --- NEW PROFESSIONAL-GRADE METRICS ---
  extreme_risk: { var_99_percent: number; max_expected_loss_usd: number }
  risk_adjusted_return: { sharpe_ratio: number }
  market_correlation: { beta: number }
  // -------------------------------------
  educational_explanation: string
}

interface ChartData {
  date: string
  price: number
  sma20: number
  sma50: number
}

export default function Home() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null)
  const [chartData, setChartData] = useState<ChartData[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const analyzeStock = async (ticker: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      // Call the live backend API
      const response = await fetch(`https://traderai-r9iz.onrender.com/api/v1/analyze/${ticker}`)
      if (!response.ok) {
        throw new Error(`Failed to analyze ${ticker}: ${response.statusText}`)
      }
      const data = await response.json()
      
      // Set the real analysis data
      setAnalysisData(data)
      
      // Generate chart data based on real analysis (simplified for demo)
      // In a real implementation, you'd get historical data from the backend
      const mockChartData: ChartData[] = []
      const basePrice = data.current_price
      const currentDate = new Date()
      
      for (let i = 29; i >= 0; i--) {
        const date = new Date(currentDate)
        date.setDate(date.getDate() - i)
        
        const priceVariation = (Math.random() - 0.5) * 10
        const price = basePrice + priceVariation + (Math.random() - 0.5) * 5
        
        mockChartData.push({
          date: date.toISOString().split('T')[0],
          price: Math.max(price, 1), // Ensure positive price
          sma20: data.sma_20 + (Math.random() - 0.5) * 8,
          sma50: data.sma_50 + (Math.random() - 0.5) * 12,
        })
      }
      
      setChartData(mockChartData)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      console.error('Analysis error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            TraderBlockAI
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-4">
            AI-Powered Stock Analysis for Educational Purposes
          </p>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-500 to-indigo-600 mx-auto rounded-full"></div>
        </div>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto space-y-8">
          {/* Ticker Input */}
          <div className="flex justify-center">
            <TickerInput onAnalyze={analyzeStock} isLoading={isLoading} />
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* Analysis Results */}
          {analysisData && (
            <>
              {/* Chart */}
              <StockChart
                data={chartData}
                currentPrice={analysisData.current_price}
                forecast={analysisData.forecast}
                isLoading={isLoading}
              />

              {/* Analysis Dashboard */}
              <AnalysisDashboard data={analysisData} isLoading={isLoading} />
            </>
          )}

          {/* Legal Disclaimer - Always Visible */}
          <Disclaimer />
        </div>

        {/* Footer */}
        <footer className="text-center mt-12 py-6 border-t border-gray-200 dark:border-gray-700">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            TraderBlockAI - Educational Stock Analysis Tool | Not Financial Advice
          </p>
        </footer>
      </div>
    </div>
  )
}
