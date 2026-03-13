"use client"

import { Brain, TrendingUp, AlertTriangle, Lightbulb, ArrowRight } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

const insights = [
  {
    type: "opportunity",
    icon: TrendingUp,
    title: "Strong Buy Signal: NVDA",
    description:
      "AI detected bullish momentum pattern with 89% historical accuracy. RSI indicating oversold conditions.",
    time: "2 min ago",
    confidence: 94,
  },
  {
    type: "warning",
    icon: AlertTriangle,
    title: "Risk Alert: Tech Sector",
    description:
      "Unusual volume detected in tech puts. Consider hedging your MSFT and GOOGL positions.",
    time: "15 min ago",
    confidence: 78,
  },
  {
    type: "insight",
    icon: Lightbulb,
    title: "Portfolio Optimization",
    description:
      "Rebalancing recommendation: Reduce bond allocation by 5% and increase emerging markets exposure.",
    time: "1 hour ago",
    confidence: 85,
  },
]

export function AIInsights() {
  return (
    <Card className="border-border bg-card">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
            <Brain className="h-4 w-4 text-primary" />
          </div>
          <CardTitle className="text-lg font-semibold text-foreground">AI Insights</CardTitle>
        </div>
        <Button variant="ghost" size="sm">
          View All
        </Button>
      </CardHeader>
      <CardContent className="space-y-4">
        {insights.map((insight, index) => (
          <div
            key={index}
            className="group relative rounded-lg border border-border bg-secondary/30 p-4 transition-all hover:border-primary/50 hover:bg-secondary/50"
          >
            <div className="flex items-start gap-3">
              <div
                className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${
                  insight.type === "opportunity"
                    ? "bg-primary/20"
                    : insight.type === "warning"
                    ? "bg-destructive/20"
                    : "bg-chart-3/20"
                }`}
              >
                <insight.icon
                  className={`h-4 w-4 ${
                    insight.type === "opportunity"
                      ? "text-primary"
                      : insight.type === "warning"
                      ? "text-destructive"
                      : "text-chart-3"
                  }`}
                />
              </div>
              <div className="flex-1">
                <div className="flex items-start justify-between">
                  <h4 className="font-medium text-foreground">{insight.title}</h4>
                  <span className="ml-2 shrink-0 text-xs text-muted-foreground">{insight.time}</span>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{insight.description}</p>
                <div className="mt-3 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground">Confidence</span>
                    <div className="h-1.5 w-20 overflow-hidden rounded-full bg-secondary">
                      <div
                        className={`h-full rounded-full ${
                          insight.confidence >= 90
                            ? "bg-primary"
                            : insight.confidence >= 80
                            ? "bg-chart-3"
                            : "bg-chart-4"
                        }`}
                        style={{ width: `${insight.confidence}%` }}
                      />
                    </div>
                    <span className="text-xs font-medium text-foreground">{insight.confidence}%</span>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="opacity-0 transition-opacity group-hover:opacity-100"
                  >
                    Details
                    <ArrowRight className="ml-1 h-3 w-3" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
