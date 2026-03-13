"use client"

import { TrendingUp, TrendingDown, DollarSign, PieChart, Activity, Zap } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

const stats = [
  {
    title: "Portfolio Value",
    value: "$284,532.00",
    change: "+12.5%",
    trend: "up",
    icon: DollarSign,
  },
  {
    title: "Today's P&L",
    value: "+$3,241.82",
    change: "+2.4%",
    trend: "up",
    icon: Activity,
  },
  {
    title: "AI Signals",
    value: "24 Active",
    change: "8 new",
    trend: "up",
    icon: Zap,
  },
  {
    title: "Win Rate",
    value: "78.4%",
    change: "+3.2%",
    trend: "up",
    icon: PieChart,
  },
]

export function StatsCards() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card
          key={stat.title}
          className="group relative overflow-hidden border-border bg-card transition-all hover:border-primary/50"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-muted-foreground">{stat.title}</p>
                <p className="mt-1 text-2xl font-bold text-foreground">{stat.value}</p>
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                <stat.icon className="h-5 w-5 text-primary" />
              </div>
            </div>
            <div className="mt-3 flex items-center gap-1.5">
              {stat.trend === "up" ? (
                <TrendingUp className="h-4 w-4 text-primary" />
              ) : (
                <TrendingDown className="h-4 w-4 text-destructive" />
              )}
              <span
                className={
                  stat.trend === "up" ? "text-sm text-primary" : "text-sm text-destructive"
                }
              >
                {stat.change}
              </span>
              <span className="text-sm text-muted-foreground">vs last month</span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
