import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'

interface ChartData {
  date: string
  price: number
  sma20: number
  sma50: number
  forecast?: number
}

interface StockChartProps {
  data: ChartData[]
  currentPrice: number
  forecast: { day_1: number; day_2: number; day_3: number }
  isLoading?: boolean
}

const StockChart: React.FC<StockChartProps> = ({ data, currentPrice, forecast, isLoading = false }) => {
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Stock Chart</CardTitle>
          <CardDescription>Loading chart data...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80 flex items-center justify-center">
            <div className="animate-pulse text-muted-foreground">Loading...</div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Stock Chart</CardTitle>
          <CardDescription>No data available</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80 flex items-center justify-center text-muted-foreground">
            Enter a ticker symbol to view the chart
          </div>
        </CardContent>
      </Card>
    )
  }

  // Add forecast data points
  const chartData = [...data]
  const lastDate = new Date(data[data.length - 1]?.date || Date.now())
  
  // Add forecast points (simplified - in real implementation, you'd get more historical data)
  chartData.push({
    date: new Date(lastDate.getTime() + 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    price: forecast.day_1,
    sma20: data[data.length - 1]?.sma20 || 0,
    sma50: data[data.length - 1]?.sma50 || 0,
    forecast: forecast.day_1
  })
  
  chartData.push({
    date: new Date(lastDate.getTime() + 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    price: forecast.day_2,
    sma20: data[data.length - 1]?.sma20 || 0,
    sma50: data[data.length - 1]?.sma50 || 0,
    forecast: forecast.day_2
  })
  
  chartData.push({
    date: new Date(lastDate.getTime() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    price: forecast.day_3,
    sma20: data[data.length - 1]?.sma20 || 0,
    sma50: data[data.length - 1]?.sma50 || 0,
    forecast: forecast.day_3
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Price Chart with AI Forecast</CardTitle>
        <CardDescription>
          Historical prices with 20-day and 50-day moving averages, plus 3-day AI forecast
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(value) => new Date(value).toLocaleDateString()}
              />
              <YAxis domain={['dataMin - 5', 'dataMax + 5']} />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleDateString()}
                formatter={(value, name) => [`$${Number(value).toFixed(2)}`, name]}
              />
              
              {/* Historical price line */}
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke="#2563eb" 
                strokeWidth={2}
                dot={false}
                name="Price"
              />
              
              {/* SMA 20 */}
              <Line 
                type="monotone" 
                dataKey="sma20" 
                stroke="#f59e0b" 
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={false}
                name="SMA 20"
              />
              
              {/* SMA 50 */}
              <Line 
                type="monotone" 
                dataKey="sma50" 
                stroke="#ef4444" 
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={false}
                name="SMA 50"
              />
              
              {/* AI Forecast line */}
              <Line 
                type="monotone" 
                dataKey="forecast" 
                stroke="#10b981" 
                strokeWidth={2}
                strokeDasharray="10 5"
                dot={false}
                name="AI Forecast"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">Current Price:</span>
            <div className="font-semibold">${currentPrice.toFixed(2)}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Day 1 Forecast:</span>
            <div className="font-semibold">${forecast.day_1.toFixed(2)}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Day 2 Forecast:</span>
            <div className="font-semibold">${forecast.day_2.toFixed(2)}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Day 3 Forecast:</span>
            <div className="font-semibold">${forecast.day_3.toFixed(2)}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default StockChart
