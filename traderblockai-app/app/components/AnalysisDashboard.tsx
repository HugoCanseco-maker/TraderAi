import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip'
import { TrendingUp, TrendingDown, Minus, Activity, BarChart3, Info } from 'lucide-react'

interface AnalysisData {
  ticker: string
  current_price: number
  trend: string
  momentum: string
  volatility: string
  confidence: number
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

interface AnalysisDashboardProps {
  data: AnalysisData | null
  isLoading?: boolean
}

const getTrendIcon = (trend: string) => {
  switch (trend.toLowerCase()) {
    case 'bullish':
      return <TrendingUp className="h-4 w-4 text-green-600" />
    case 'bearish':
      return <TrendingDown className="h-4 w-4 text-red-600" />
    default:
      return <Minus className="h-4 w-4 text-yellow-600" />
  }
}

const getTrendColor = (trend: string) => {
  switch (trend.toLowerCase()) {
    case 'bullish':
      return 'text-green-600'
    case 'bearish':
      return 'text-red-600'
    default:
      return 'text-yellow-600'
  }
}

const getMomentumColor = (momentum: string) => {
  switch (momentum.toLowerCase()) {
    case 'overbought':
    case 'positive':
      return 'text-green-600'
    case 'oversold':
    case 'negative':
      return 'text-red-600'
    default:
      return 'text-yellow-600'
  }
}

const getVolatilityColor = (volatility: string) => {
  switch (volatility.toLowerCase()) {
    case 'high':
      return 'text-red-600'
    case 'medium':
      return 'text-yellow-600'
    case 'low':
      return 'text-green-600'
    default:
      return 'text-gray-600'
  }
}

const AnalysisDashboard: React.FC<AnalysisDashboardProps> = ({ data, isLoading = false }) => {
  if (isLoading) {
    return (
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>AI Analysis</CardTitle>
            <CardDescription>Loading analysis...</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="animate-pulse space-y-4">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Learning Corner</CardTitle>
            <CardDescription>Loading explanation...</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="animate-pulse space-y-3">
              <div className="h-4 bg-gray-200 rounded"></div>
              <div className="h-4 bg-gray-200 rounded w-4/5"></div>
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>AI Analysis</CardTitle>
            <CardDescription>No analysis data available</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">Enter a ticker symbol to get AI-powered analysis</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Learning Corner</CardTitle>
            <CardDescription>Educational insights will appear here</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">Analysis explanation will be displayed here</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <TooltipProvider>
      <div className="grid gap-6 md:grid-cols-2">
        {/* AI Analysis Panel */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5" />
              AI Analysis for {data.ticker}
            </CardTitle>
            <CardDescription>
              Current price: ${data.current_price.toFixed(2)} | Confidence: {(data.confidence * 100).toFixed(0)}%
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Trend Analysis */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-medium">Trend</span>
                <Tooltip>
                  <TooltipTrigger>
                    <Info className="h-4 w-4 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Overall price direction based on moving averages and price action</p>
                  </TooltipContent>
                </Tooltip>
              </div>
              <div className={`flex items-center gap-2 font-semibold ${getTrendColor(data.trend)}`}>
                {getTrendIcon(data.trend)}
                {data.trend}
              </div>
            </div>

            {/* Momentum Analysis */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-medium">Momentum</span>
                <Tooltip>
                  <TooltipTrigger>
                    <Info className="h-4 w-4 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Price momentum based on RSI and MACD indicators</p>
                  </TooltipContent>
                </Tooltip>
              </div>
              <div className={`font-semibold ${getMomentumColor(data.momentum)}`}>
                {data.momentum}
              </div>
            </div>

            {/* Volatility Analysis */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-medium">Volatility</span>
                <Tooltip>
                  <TooltipTrigger>
                    <Info className="h-4 w-4 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Price volatility based on historical price movements</p>
                  </TooltipContent>
                </Tooltip>
              </div>
              <div className={`font-semibold ${getVolatilityColor(data.volatility)}`}>
                {data.volatility}
              </div>
            </div>

            {/* Technical Indicators */}
            <div className="border-t pt-4">
              <h4 className="font-medium mb-3 flex items-center gap-2">
                <BarChart3 className="h-4 w-4" />
                Technical Indicators
              </h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">SMA 20:</span>
                  <div className="font-semibold">${data.sma_20.toFixed(2)}</div>
                </div>
                <div>
                  <span className="text-muted-foreground">SMA 50:</span>
                  <div className="font-semibold">${data.sma_50.toFixed(2)}</div>
                </div>
                <div>
                  <span className="text-muted-foreground">RSI:</span>
                  <div className="font-semibold">{data.rsi.toFixed(1)}</div>
                </div>
                <div>
                  <span className="text-muted-foreground">MACD:</span>
                  <div className="font-semibold">{data.macd.toFixed(3)}</div>
                </div>
              </div>
            </div>

            {/* Professional-Grade Risk Metrics */}
            <div className="border-t pt-4">
              <h4 className="font-medium mb-3 flex items-center gap-2">
                <Activity className="h-4 w-4" />
                Professional Risk Metrics
              </h4>
              <div className="grid grid-cols-1 gap-4 text-sm">
                {/* Value at Risk */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground">VaR (99%):</span>
                    <Tooltip>
                      <TooltipTrigger>
                        <Info className="h-3 w-3 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Value at Risk - potential worst-case daily loss</p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                  <div className="font-semibold text-red-600">
                    ${Math.abs(data.extreme_risk.max_expected_loss_usd).toFixed(2)}
                  </div>
                </div>
                
                {/* Sharpe Ratio */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground">Sharpe Ratio:</span>
                    <Tooltip>
                      <TooltipTrigger>
                        <Info className="h-3 w-3 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Risk-adjusted return measure</p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                  <div className={`font-semibold ${data.risk_adjusted_return.sharpe_ratio > 1 ? 'text-green-600' : data.risk_adjusted_return.sharpe_ratio > 0 ? 'text-yellow-600' : 'text-red-600'}`}>
                    {data.risk_adjusted_return.sharpe_ratio.toFixed(2)}
                  </div>
                </div>
                
                {/* Beta */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground">Beta:</span>
                    <Tooltip>
                      <TooltipTrigger>
                        <Info className="h-3 w-3 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Market correlation - how stock moves vs S&P 500</p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                  <div className={`font-semibold ${data.market_correlation.beta > 1 ? 'text-red-600' : data.market_correlation.beta < 1 ? 'text-green-600' : 'text-yellow-600'}`}>
                    {data.market_correlation.beta.toFixed(2)}
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Learning Corner */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Learning Corner
            </CardTitle>
            <CardDescription>
              Understanding the analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="prose prose-sm max-w-none">
              <p className="text-sm leading-relaxed">
                {data.educational_explanation}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </TooltipProvider>
  )
}

export default AnalysisDashboard
