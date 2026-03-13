"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  Area,
  AreaChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts"

const data = [
  { date: "Jan", value: 210000, ai: 195000 },
  { date: "Feb", value: 218000, ai: 205000 },
  { date: "Mar", value: 205000, ai: 215000 },
  { date: "Apr", value: 235000, ai: 230000 },
  { date: "May", value: 248000, ai: 255000 },
  { date: "Jun", value: 262000, ai: 268000 },
  { date: "Jul", value: 255000, ai: 275000 },
  { date: "Aug", value: 278000, ai: 285000 },
  { date: "Sep", value: 284532, ai: 292000 },
]

const timeRanges = ["24H", "1W", "1M", "3M", "1Y", "ALL"]

export function PortfolioChart() {
  return (
    <Card className="border-border bg-card">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div>
          <CardTitle className="text-lg font-semibold text-foreground">Portfolio Performance</CardTitle>
          <p className="text-sm text-muted-foreground">Your portfolio vs AI predictions</p>
        </div>
        <div className="flex gap-1">
          {timeRanges.map((range) => (
            <Button
              key={range}
              variant={range === "1Y" ? "secondary" : "ghost"}
              size="sm"
              className={range === "1Y" ? "bg-primary/10 text-primary hover:bg-primary/20" : ""}
            >
              {range}
            </Button>
          ))}
        </div>
      </CardHeader>
      <CardContent className="pt-4">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="portfolioGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="oklch(0.72 0.19 163)" stopOpacity={0.4} />
                <stop offset="100%" stopColor="oklch(0.72 0.19 163)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="aiGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="oklch(0.65 0.15 250)" stopOpacity={0.3} />
                <stop offset="100%" stopColor="oklch(0.65 0.15 250)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="date"
              axisLine={false}
              tickLine={false}
              tick={{ fill: "oklch(0.65 0 0)", fontSize: 12 }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: "oklch(0.65 0 0)", fontSize: 12 }}
              tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "oklch(0.16 0.01 260)",
                border: "1px solid oklch(0.28 0.01 260)",
                borderRadius: "8px",
                color: "oklch(0.98 0 0)",
              }}
              formatter={(value: number) => [`$${value.toLocaleString()}`, ""]}
            />
            <Area
              type="monotone"
              dataKey="ai"
              stroke="oklch(0.65 0.15 250)"
              strokeWidth={2}
              fill="url(#aiGradient)"
              strokeDasharray="5 5"
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="oklch(0.72 0.19 163)"
              strokeWidth={2}
              fill="url(#portfolioGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
        <div className="mt-4 flex items-center justify-center gap-6">
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 rounded-full bg-primary" />
            <span className="text-sm text-muted-foreground">Your Portfolio</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 rounded-full bg-chart-2" />
            <span className="text-sm text-muted-foreground">AI Prediction</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
