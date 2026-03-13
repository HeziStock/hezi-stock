"use client"

import { Button } from "@/components/ui/button"
import { ArrowRight, Play, TrendingUp, Zap, BarChart3 } from "lucide-react"

export function Hero() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
      {/* Gradient background effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-chart-2/10 rounded-full blur-3xl" />
      
      {/* Floating stock indicators */}
      <div className="absolute top-20 left-[10%] hidden lg:flex items-center gap-2 px-4 py-2 bg-card/80 backdrop-blur border border-border rounded-full animate-pulse">
        <TrendingUp className="w-4 h-4 text-primary" />
        <span className="text-sm font-medium">AAPL +2.4%</span>
      </div>
      <div className="absolute top-40 right-[15%] hidden lg:flex items-center gap-2 px-4 py-2 bg-card/80 backdrop-blur border border-border rounded-full">
        <BarChart3 className="w-4 h-4 text-chart-3" />
        <span className="text-sm font-medium">NVDA +5.1%</span>
      </div>
      <div className="absolute bottom-32 left-[15%] hidden lg:flex items-center gap-2 px-4 py-2 bg-card/80 backdrop-blur border border-border rounded-full">
        <Zap className="w-4 h-4 text-chart-2" />
        <span className="text-sm font-medium">AI Scan Active</span>
      </div>

      <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 mb-8 bg-primary/10 border border-primary/20 rounded-full">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
          </span>
          <span className="text-sm font-medium text-primary">No signup required</span>
        </div>

        {/* Main headline */}
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 text-balance">
          Find winning stocks
          <span className="block mt-2 bg-gradient-to-r from-primary via-chart-2 to-primary bg-clip-text text-transparent">
            faster.
          </span>
        </h1>

        {/* Subheadline */}
        <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 text-pretty">
          AI-assisted market scans deliver a ranked shortlist of up to 10 daily ideas 
          with ratings and a short "why enter now". No signup required.
        </p>

        {/* CTA buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Button size="lg" className="group px-8 py-6 text-lg bg-primary hover:bg-primary/90">
            Open Dashboard
            <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Button>
          <Button size="lg" variant="outline" className="px-8 py-6 text-lg border-border hover:bg-secondary">
            <Play className="mr-2 w-5 h-5" />
            See Reports
          </Button>
        </div>

        {/* Stats */}
        <div className="flex flex-wrap items-center justify-center gap-8 sm:gap-12 mt-16 pt-8 border-t border-border/50">
          <div className="text-center">
            <div className="text-3xl sm:text-4xl font-bold text-foreground">10</div>
            <div className="text-sm text-muted-foreground mt-1">Daily Ideas</div>
          </div>
          <div className="text-center">
            <div className="text-3xl sm:text-4xl font-bold text-primary">1-10</div>
            <div className="text-sm text-muted-foreground mt-1">AI Ratings</div>
          </div>
          <div className="text-center">
            <div className="text-3xl sm:text-4xl font-bold text-foreground">{'<'}5s</div>
            <div className="text-sm text-muted-foreground mt-1">Scan Time</div>
          </div>
          <div className="text-center">
            <div className="text-3xl sm:text-4xl font-bold text-chart-3">Free</div>
            <div className="text-sm text-muted-foreground mt-1">No Card</div>
          </div>
        </div>
      </div>
    </section>
  )
}
