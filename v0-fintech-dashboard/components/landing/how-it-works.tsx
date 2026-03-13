"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Scan, Brain, Rocket } from "lucide-react"

const steps = [
  {
    step: "01",
    icon: Scan,
    title: "Scan",
    subtitle: "Market movers",
    description: "We fetch gainers & losers and relevant market data from multiple sources in real-time.",
    color: "primary",
  },
  {
    step: "02",
    icon: Brain,
    title: "Rank",
    subtitle: "AI scoring",
    description: "Each idea gets a 1-10 rating and a short 'why enter now' explanation.",
    color: "chart-2",
  },
  {
    step: "03",
    icon: Rocket,
    title: "Act",
    subtitle: "Export & research",
    description: "Open any symbol on Yahoo or export CSV for your trading workflow.",
    color: "chart-3",
  },
]

export function HowItWorks() {
  return (
    <section className="py-24 px-6 bg-gradient-to-b from-secondary/30 to-transparent">
      <div className="max-w-6xl mx-auto">
        {/* Section header */}
        <div className="text-center mb-16">
          <span className="inline-block px-4 py-1.5 mb-4 text-sm font-medium bg-primary/10 text-primary rounded-full">
            How it works
          </span>
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Three simple steps to
            <span className="text-primary"> better trades</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Our streamlined process gets you from market data to actionable insights in seconds.
          </p>
        </div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <Card 
              key={index} 
              className="relative border-border bg-card/50 backdrop-blur overflow-hidden group hover:border-primary/50 transition-all duration-300"
            >
              {/* Step number background */}
              <div className="absolute -top-6 -right-6 text-[120px] font-bold text-border/30 select-none">
                {step.step}
              </div>
              
              <CardContent className="relative p-8">
                {/* Icon */}
                <div className={`inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-${step.color}/10 text-${step.color} mb-6`}>
                  <step.icon className="w-7 h-7" />
                </div>
                
                {/* Content */}
                <div className="space-y-2">
                  <div className="flex items-center gap-3">
                    <span className={`text-xs font-semibold uppercase tracking-wider text-${step.color}`}>
                      Step {step.step}
                    </span>
                  </div>
                  <h3 className="text-2xl font-bold">{step.title}</h3>
                  <p className="text-sm font-medium text-muted-foreground">{step.subtitle}</p>
                  <p className="text-muted-foreground pt-2">{step.description}</p>
                </div>
              </CardContent>

              {/* Connector line for desktop */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gradient-to-r from-border to-transparent" />
              )}
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
