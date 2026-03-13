"use client"

import { useState } from "react"
import { Play, Download, TrendingUp, TrendingDown, Sparkles, Clock, RefreshCw, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Navbar } from "@/components/landing/navbar"

// Mock data for demonstration
const mockStocks = [
  { rank: 1, ticker: "NVDA", name: "NVIDIA Corp", price: 892.45, change: 4.2, rating: "Strong Buy", score: 95, reasoning: "AI chip demand surge, strong earnings momentum" },
  { rank: 2, ticker: "MSFT", name: "Microsoft Corp", price: 425.22, change: 2.1, rating: "Buy", score: 88, reasoning: "Cloud growth acceleration, AI integration" },
  { rank: 3, ticker: "AAPL", name: "Apple Inc", price: 178.92, change: 1.5, rating: "Buy", score: 85, reasoning: "Services revenue growth, iPhone cycle" },
  { rank: 4, ticker: "GOOGL", name: "Alphabet Inc", price: 141.80, change: 3.2, rating: "Buy", score: 82, reasoning: "Search dominance, Gemini AI rollout" },
  { rank: 5, ticker: "META", name: "Meta Platforms", price: 505.75, change: -0.8, rating: "Hold", score: 75, reasoning: "Ad revenue recovery, Metaverse costs" },
  { rank: 6, ticker: "AMZN", name: "Amazon.com", price: 178.25, change: 1.8, rating: "Buy", score: 80, reasoning: "AWS growth, retail margins improving" },
  { rank: 7, ticker: "TSLA", name: "Tesla Inc", price: 245.30, change: -2.1, rating: "Hold", score: 68, reasoning: "EV competition, margin pressure" },
  { rank: 8, ticker: "AMD", name: "AMD Inc", price: 156.80, change: 5.2, rating: "Strong Buy", score: 91, reasoning: "Data center gains, AI chip expansion" },
  { rank: 9, ticker: "CRM", name: "Salesforce", price: 275.40, change: 1.2, rating: "Buy", score: 78, reasoning: "Enterprise AI adoption, margin expansion" },
  { rank: 10, ticker: "NFLX", name: "Netflix Inc", price: 628.90, change: 0.9, rating: "Hold", score: 72, reasoning: "Subscriber growth, ad tier momentum" },
]

export default function DashboardPage() {
  const [hasReport, setHasReport] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [lastUpdated, setLastUpdated] = useState<string | null>(null)

  const runScan = () => {
    setIsLoading(true)
    // Simulate API call
    setTimeout(() => {
      setHasReport(true)
      setIsLoading(false)
      setLastUpdated(new Date().toLocaleTimeString())
    }, 2000)
  }

  const exportCSV = () => {
    const headers = ["Rank", "Ticker", "Name", "Price", "Change %", "Rating", "Score", "Reasoning"]
    const rows = mockStocks.map(s => [s.rank, s.ticker, s.name, s.price, s.change, s.rating, s.score, s.reasoning])
    const csv = [headers, ...rows].map(r => r.join(",")).join("\n")
    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `hezi-stock-report-${new Date().toISOString().split("T")[0]}.csv`
    a.click()
  }

  const getRatingColor = (rating: string) => {
    switch (rating) {
      case "Strong Buy": return "text-emerald-400 bg-emerald-400/10"
      case "Buy": return "text-green-400 bg-green-400/10"
      case "Hold": return "text-yellow-400 bg-yellow-400/10"
      case "Sell": return "text-red-400 bg-red-400/10"
      default: return "text-muted-foreground bg-muted"
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="pt-24 pb-16 px-4">
        <div className="max-w-7xl mx-auto">
          {/* Header Section */}
          <div className="mb-8">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
                  Dashboard
                </h1>
                <p className="text-muted-foreground">
                  Run market scans, view top 10 recommendations & export CSV.
                </p>
              </div>
              
              <div className="flex items-center gap-3">
                {hasReport && (
                  <Button 
                    variant="outline" 
                    onClick={exportCSV}
                    className="border-border hover:bg-secondary"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Export CSV
                  </Button>
                )}
                <Button 
                  onClick={runScan}
                  disabled={isLoading}
                  className="bg-primary hover:bg-primary/90 text-primary-foreground"
                >
                  {isLoading ? (
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    <Play className="w-4 h-4 mr-2" />
                  )}
                  {isLoading ? "Scanning..." : "Run now"}
                </Button>
              </div>
            </div>
            
            {lastUpdated && (
              <div className="flex items-center gap-2 mt-4 text-sm text-muted-foreground">
                <Clock className="w-4 h-4" />
                Last updated: {lastUpdated}
              </div>
            )}
          </div>

          {/* Content Area */}
          {!hasReport ? (
            <Card className="bg-card border-border">
              <CardContent className="flex flex-col items-center justify-center py-20">
                <div className="w-20 h-20 rounded-full bg-secondary flex items-center justify-center mb-6">
                  <FileText className="w-10 h-10 text-muted-foreground" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">No report yet</h3>
                <p className="text-muted-foreground text-center max-w-md mb-6">
                  Click <span className="text-primary font-medium">Run now</span> above to fetch market movers and build your first insight with up to 10 entry recommendations.
                </p>
                <Button 
                  onClick={runScan}
                  disabled={isLoading}
                  className="bg-primary hover:bg-primary/90 text-primary-foreground"
                >
                  {isLoading ? (
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    <Sparkles className="w-4 h-4 mr-2" />
                  )}
                  Run your first report
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6">
              {/* Stats Overview */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="bg-card border-border">
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-foreground">Strong Buy Signals</p>
                        <p className="text-3xl font-bold text-emerald-400">2</p>
                      </div>
                      <div className="w-12 h-12 rounded-full bg-emerald-400/10 flex items-center justify-center">
                        <TrendingUp className="w-6 h-6 text-emerald-400" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
                
                <Card className="bg-card border-border">
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-foreground">Buy Signals</p>
                        <p className="text-3xl font-bold text-green-400">4</p>
                      </div>
                      <div className="w-12 h-12 rounded-full bg-green-400/10 flex items-center justify-center">
                        <TrendingUp className="w-6 h-6 text-green-400" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
                
                <Card className="bg-card border-border">
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-foreground">Hold Signals</p>
                        <p className="text-3xl font-bold text-yellow-400">4</p>
                      </div>
                      <div className="w-12 h-12 rounded-full bg-yellow-400/10 flex items-center justify-center">
                        <TrendingDown className="w-6 h-6 text-yellow-400" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Recommendations Table */}
              <Card className="bg-card border-border overflow-hidden">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-primary" />
                    Top 10 Recommendations
                  </CardTitle>
                  <CardDescription>
                    AI-ranked stock ideas based on today's market analysis
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-border bg-secondary/50">
                          <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Rank</th>
                          <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Ticker</th>
                          <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground hidden md:table-cell">Name</th>
                          <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Price</th>
                          <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Change</th>
                          <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground">Rating</th>
                          <th className="text-center py-3 px-4 text-sm font-medium text-muted-foreground hidden lg:table-cell">Score</th>
                          <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground hidden xl:table-cell">Reasoning</th>
                        </tr>
                      </thead>
                      <tbody>
                        {mockStocks.map((stock) => (
                          <tr 
                            key={stock.ticker} 
                            className="border-b border-border last:border-0 hover:bg-secondary/30 transition-colors"
                          >
                            <td className="py-4 px-4">
                              <span className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-sm font-medium text-foreground">
                                {stock.rank}
                              </span>
                            </td>
                            <td className="py-4 px-4">
                              <span className="font-semibold text-foreground">{stock.ticker}</span>
                            </td>
                            <td className="py-4 px-4 text-muted-foreground hidden md:table-cell">
                              {stock.name}
                            </td>
                            <td className="py-4 px-4 text-right font-medium text-foreground">
                              ${stock.price.toFixed(2)}
                            </td>
                            <td className="py-4 px-4 text-right">
                              <span className={`font-medium ${stock.change >= 0 ? "text-emerald-400" : "text-red-400"}`}>
                                {stock.change >= 0 ? "+" : ""}{stock.change}%
                              </span>
                            </td>
                            <td className="py-4 px-4 text-center">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRatingColor(stock.rating)}`}>
                                {stock.rating}
                              </span>
                            </td>
                            <td className="py-4 px-4 text-center hidden lg:table-cell">
                              <div className="flex items-center justify-center gap-2">
                                <div className="w-16 h-2 bg-secondary rounded-full overflow-hidden">
                                  <div 
                                    className="h-full bg-primary rounded-full"
                                    style={{ width: `${stock.score}%` }}
                                  />
                                </div>
                                <span className="text-sm text-muted-foreground">{stock.score}</span>
                              </div>
                            </td>
                            <td className="py-4 px-4 text-muted-foreground text-sm hidden xl:table-cell max-w-xs truncate">
                              {stock.reasoning}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
