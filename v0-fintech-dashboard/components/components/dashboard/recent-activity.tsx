"use client"

import { ArrowUpRight, ArrowDownRight, Clock } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

const activities = [
  {
    type: "buy",
    symbol: "NVDA",
    shares: 15,
    price: 875.38,
    total: 13130.7,
    time: "Today, 10:42 AM",
    aiAssisted: true,
  },
  {
    type: "sell",
    symbol: "GOOGL",
    shares: 8,
    price: 142.56,
    total: 1140.48,
    time: "Today, 9:15 AM",
    aiAssisted: false,
  },
  {
    type: "buy",
    symbol: "AAPL",
    shares: 25,
    price: 176.28,
    total: 4407.0,
    time: "Yesterday, 3:30 PM",
    aiAssisted: true,
  },
  {
    type: "buy",
    symbol: "MSFT",
    shares: 10,
    price: 415.82,
    total: 4158.2,
    time: "Yesterday, 11:20 AM",
    aiAssisted: false,
  },
]

export function RecentActivity() {
  return (
    <Card className="border-border bg-card">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-lg font-semibold text-foreground">Recent Activity</CardTitle>
        <Button variant="ghost" size="sm">
          View All
        </Button>
      </CardHeader>
      <CardContent className="space-y-4">
        {activities.map((activity, index) => (
          <div
            key={index}
            className="flex items-center justify-between rounded-lg border border-border bg-secondary/30 p-3"
          >
            <div className="flex items-center gap-3">
              <div
                className={`flex h-9 w-9 items-center justify-center rounded-lg ${
                  activity.type === "buy" ? "bg-primary/20" : "bg-destructive/20"
                }`}
              >
                {activity.type === "buy" ? (
                  <ArrowUpRight className="h-4 w-4 text-primary" />
                ) : (
                  <ArrowDownRight className="h-4 w-4 text-destructive" />
                )}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-foreground">
                    {activity.type === "buy" ? "Bought" : "Sold"} {activity.symbol}
                  </span>
                  {activity.aiAssisted && (
                    <span className="rounded bg-primary/20 px-1.5 py-0.5 text-[10px] font-medium text-primary">
                      AI
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <span>{activity.shares} shares @ ${activity.price.toFixed(2)}</span>
                </div>
              </div>
            </div>
            <div className="text-right">
              <p
                className={`font-medium ${
                  activity.type === "buy" ? "text-foreground" : "text-foreground"
                }`}
              >
                {activity.type === "buy" ? "-" : "+"}${activity.total.toLocaleString()}
              </p>
              <div className="flex items-center justify-end gap-1 text-sm text-muted-foreground">
                <Clock className="h-3 w-3" />
                <span>{activity.time}</span>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
