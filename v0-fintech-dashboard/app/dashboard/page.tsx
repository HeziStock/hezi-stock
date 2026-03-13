"use client"

import { useState, useEffect, useCallback } from "react"
import { Play, Download, TrendingUp, TrendingDown, Sparkles, Clock, RefreshCw, FileText, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Navbar } from "@/components/landing/navbar"

const API_BASE = typeof process !== "undefined" && process.env.NEXT_PUBLIC_HEZI_STOCK_API
  ? process.env.NEXT_PUBLIC_HEZI_STOCK_API
  : "http://localhost:5000"

type Recommendation = {
  symbol: string
  name?: string
  price?: number
  change_pct?: number
  reason?: string
  why_enter_now?: string
  rating?: number
}

function ratingToLabel(rating: number): string {
  if (rating >= 9) return "Strong Buy"
  if (rating >= 7) return "Buy"
  if (rating >= 5) return "Hold"
  if (rating >= 3) return "Underperform"
  return "Sell"
}

export default function DashboardPage() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [generatedAt, setGeneratedAt] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const loadRecommendations = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/api/recommendations`)
      const data = await res.json()
      if (!res.ok) throw new Error(data.message || "Failed to load")
      if (data.ok && Array.isArray(data.recommendations)) {
        setRecommendations(data.recommendations)
        setGeneratedAt(data.generated_at || null)
      } else {
        setRecommendations([])
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not reach HEZI STOCK. Is the portal running?")
      setRecommendations([])
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => { loadRecommendations() }, [loadRecommendations])

  const runScan = () => loadRecommendations()

  const exportCSV = () => {
    const headers = ["Rank", "Symbol", "Name", "Rating", "Price", "Change %", "Reason", "Why enter now"]
    const rows = recommendations.map((r, i) => [
      i + 1,
      r.symbol,
      r.name || "",
      r.rating ?? "",
      r.price ?? "",
      r.change_pct ?? "",
      (r.reason || "").slice(0, 200),
      (r.why_enter_now || r.reason || "").slice(0, 200),
    ])
    const csv = [headers, ...rows].map(r => r.join(",")).join("\n")
    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `hezi-stock-report-${new Date().toISOString().split("T")[0]}.csv`
    a.click()
  }

  const getRatingColor = (rating: number | undefined) => {
    if (rating == null) return "text-muted-foreground bg-muted"
    const label = ratingToLabel(rating)
    switch (label) {
      case "Strong Buy": return "text-emerald-400 bg-emerald-400/10"
      case "Buy": return "text-green-400 bg-green-400/10"
      case "Hold": return "text-yellow-400 bg-yellow-400/10"
      case "Sell": return "text-red-400 bg-red-400/10"
      default: return "text-muted-foreground bg-muted"
    }
  }

  const hasReport = recommendations.length > 0

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
                  The 10 stocks most worth entering right now — from HEZI STOCK scan.
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
            
            {(generatedAt || error) && (
              <div className="flex items-center gap-2 mt-4 text-sm text-muted-foreground">
                {generatedAt && <><Clock className="w-4 h-4" /> Scan: {generatedAt.slice(0, 16).replace("T", " ")}</>}
                {error && <span className="text-destructive">{error}</span>}
              </div>
            )}
          </div>

          {/* Content Area */}
          {!hasReport && !isLoading && !error ? (
            <Card className="bg-card border-border">
              <CardContent className="flex flex-col items-center justify-center py-20">
                <div className="w-20 h-20 rounded-full bg-secondary flex items-center justify-center mb-6">
                  <FileText className="w-10 h-10 text-muted-foreground" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">No scan yet</h3>
                <p className="text-muted-foreground text-center max-w-md mb-6">
                  Run a scan in the HEZI STOCK portal to get the 10 stocks most worth entering today. Then click <span className="text-primary font-medium">Run now</span> here to refresh.
                </p>
                <a href={`${API_BASE}/app`} target="_blank" rel="noopener noreferrer">
                  <Button variant="outline" className="gap-2">
                    <ExternalLink className="w-4 h-4" />
                    Open HEZI STOCK portal
                  </Button>
                </a>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6">
              {isLoading && !hasReport ? (
                <Card className="bg-card border-border">
                  <CardContent className="flex items-center justify-center py-20">
                    <RefreshCw className="w-10 h-10 animate-spin text-muted-foreground mr-3" />
                    <span className="text-muted-foreground">Loading recommendations from HEZI STOCK…</span>
                  </CardContent>
                </Card>
              ) : hasReport ? (
                <>
                  {/* Stats from real data */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card className="bg-card border-border">
                      <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-sm text-muted-foreground">Strong Buy (9–10)</p>
                            <p className="text-3xl font-bold text-emerald-400">
                              {recommendations.filter(r => (r.rating ?? 0) >= 9).length}
                            </p>
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
                            <p className="text-sm text-muted-foreground">Buy (7–8)</p>
                            <p className="text-3xl font-bold text-green-400">
                              {recommendations.filter(r => { const x = r.rating ?? 0; return x >= 7 && x < 9; }).length}
                            </p>
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
                            <p className="text-sm text-muted-foreground">Hold (5–6)</p>
                            <p className="text-3xl font-bold text-yellow-400">
                              {recommendations.filter(r => { const x = r.rating ?? 0; return x >= 5 && x < 7; }).length}
                            </p>
                          </div>
                          <div className="w-12 h-12 rounded-full bg-yellow-400/10 flex items-center justify-center">
                            <TrendingDown className="w-6 h-6 text-yellow-400" />
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Recommendations Table — from scan */}
                  <Card className="bg-card border-border overflow-hidden">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-primary" />
                        The 10 stocks most worth entering right now
                      </CardTitle>
                      <CardDescription>
                        From today&apos;s market scan (momentum, volume &amp; analyst). Not a fixed list.
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
                              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground hidden xl:table-cell">Reason</th>
                            </tr>
                          </thead>
                          <tbody>
                            {recommendations.map((rec, idx) => (
                              <tr 
                                key={rec.symbol} 
                                className="border-b border-border last:border-0 hover:bg-secondary/30 transition-colors"
                              >
                                <td className="py-4 px-4">
                                  <span className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-sm font-medium text-foreground">
                                    {idx + 1}
                                  </span>
                                </td>
                                <td className="py-4 px-4">
                                  <a href={`https://finance.yahoo.com/quote/${rec.symbol}`} target="_blank" rel="noopener noreferrer" className="font-semibold text-foreground hover:underline">
                                    {rec.symbol}
                                  </a>
                                </td>
                                <td className="py-4 px-4 text-muted-foreground hidden md:table-cell">
                                  {rec.name ?? rec.symbol}
                                </td>
                                <td className="py-4 px-4 text-right font-medium text-foreground">
                                  {rec.price != null ? `$${Number(rec.price).toFixed(2)}` : "—"}
                                </td>
                                <td className="py-4 px-4 text-right">
                                  {rec.change_pct != null ? (
                                    <span className={`font-medium ${rec.change_pct >= 0 ? "text-emerald-400" : "text-red-400"}`}>
                                      {rec.change_pct >= 0 ? "+" : ""}{rec.change_pct}%
                                    </span>
                                  ) : "—"}
                                </td>
                                <td className="py-4 px-4 text-center">
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRatingColor(rec.rating)}`}>
                                    {rec.rating != null ? `${ratingToLabel(rec.rating)} (${rec.rating}/10)` : "—"}
                                  </span>
                                </td>
                                <td className="py-4 px-4 text-muted-foreground text-sm hidden xl:table-cell max-w-xs truncate">
                                  {rec.reason ?? rec.why_enter_now ?? "—"}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </CardContent>
                  </Card>
                </>
              ) : (
                <Card className="bg-card border-border">
                  <CardContent className="py-10 text-center text-muted-foreground">
                    {error || "No recommendations. Run a scan in the HEZI STOCK portal first."}
                    <div className="mt-4">
                      <a href={`${API_BASE}/app`} target="_blank" rel="noopener noreferrer">
                        <Button variant="outline" className="gap-2">
                          <ExternalLink className="w-4 h-4" />
                          Open portal
                        </Button>
                      </a>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
