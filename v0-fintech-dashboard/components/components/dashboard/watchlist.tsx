"use client"

import { TrendingUp, TrendingDown, MoreHorizontal } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  Line,
  LineChart,
} from "recharts"

const watchlistItems = [
  {
    symbol: "AAPL",
    name: "Apple Inc.",
    price: 178.42,
    change: 2.34,
    changePercent: 1.33,
    trend: "up",
    data: [10, 12, 8, 14, 12, 16, 15, 18, 17, 20],
    aiScore: 92,
  },
  {
    symbol: "NVDA",
    name: "NVIDIA Corp",
    price: 875.38,
    change: 24.56,
    changePercent: 2.89,
    trend: "up",
    data: [8, 10, 12, 11, 15, 14, 18, 20, 19, 24],
    aiScore: 96,
  },
  {
    symbol: "MSFT",
    name: "Microsoft",
    price: 412.65,
    change: -3.21,
    changePercent: -0.77,
    trend: "down",
    data: [20, 18, 19, 17, 16, 18, 15, 14, 16, 15],
    aiScore: 78,
  },
  {
    symbol: "TSLA",
    name: "Tesla Inc.",
    price: 242.18,
    change: 8.92,
    changePercent: 3.82,
    trend: "up",
    data: [10, 8, 12, 14, 11, 16, 18, 15, 20, 22],
    aiScore: 84,
  },
  {
    symbol: "AMZN",
    name: "Amazon.com",
    price: 178.25,
    change: 1.87,
    changePercent: 1.06,
    trend: "up",
    data: [12, 14, 13, 15, 16, 14, 17, 18, 17, 19],
    aiScore: 88,
  },
]

function MiniChart({ data, trend }: { data: number[]; trend: string }) {
  const chartData = data.map((value, index) => ({ value, index }))
  const color = trend === "up" ? "oklch(0.72 0.19 163)" : "oklch(0.65 0.2 25)"

  return (
    <LineChart width={80} height={32} data={chartData}>
      <Line
        type="monotone"
        dataKey="value"
        stroke={color}
        strokeWidth={1.5}
        dot={false}
      />
    </LineChart>
  )
}

export function Watchlist() {
  return (
    <Card className="border-border bg-card">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-lg font-semibold text-foreground">Watchlist</CardTitle>
        <Button variant="ghost" size="sm">
          View All
        </Button>
      </CardHeader>
      <CardContent className="p-0">
        <div className="divide-y divide-border">
          {watchlistItems.map((stock) => (
            <div
              key={stock.symbol}
              className="flex items-center justify-between px-6 py-4 transition-colors hover:bg-secondary/50"
            >
              <div className="flex items-center gap-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary font-semibold text-foreground">
                  {stock.symbol.slice(0, 2)}
                </div>
                <div>
                  <p className="font-medium text-foreground">{stock.symbol}</p>
                  <p className="text-sm text-muted-foreground">{stock.name}</p>
                </div>
              </div>

              <div className="hidden sm:block">
                <MiniChart data={stock.data} trend={stock.trend} />
              </div>

              <div className="flex items-center gap-2">
                <div
                  className={`flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ${
                    stock.aiScore >= 90
                      ? "bg-primary/20 text-primary"
                      : stock.aiScore >= 80
                      ? "bg-chart-3/20 text-chart-3"
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  AI: {stock.aiScore}
                </div>
              </div>

              <div className="text-right">
                <p className="font-medium text-foreground">${stock.price.toFixed(2)}</p>
                <div className="flex items-center justify-end gap-1">
                  {stock.trend === "up" ? (
                    <TrendingUp className="h-3 w-3 text-primary" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-destructive" />
                  )}
                  <span
                    className={
                      stock.trend === "up"
                        ? "text-sm text-primary"
                        : "text-sm text-destructive"
                    }
                  >
                    {stock.trend === "up" ? "+" : ""}
                    {stock.changePercent.toFixed(2)}%
                  </span>
                </div>
              </div>

              <Button variant="ghost" size="icon" className="hidden lg:flex">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
