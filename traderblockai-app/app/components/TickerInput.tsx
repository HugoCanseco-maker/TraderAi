import React, { useState } from 'react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface TickerInputProps {
  onAnalyze: (ticker: string) => void
  isLoading: boolean
}

const TickerInput: React.FC<TickerInputProps> = ({ onAnalyze, isLoading }) => {
  const [ticker, setTicker] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (ticker.trim()) {
      onAnalyze(ticker.trim().toUpperCase())
    }
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-center">Stock Analysis</CardTitle>
        <CardDescription className="text-center">
          Enter a stock ticker symbol to get AI-powered analysis
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex space-x-2">
            <Input
              type="text"
              placeholder="e.g., AAPL, MSFT, GOOGL"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              className="flex-1"
            />
            <Button type="submit" disabled={isLoading || !ticker.trim()}>
              {isLoading ? 'Analyzing...' : 'Analyze'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default TickerInput
