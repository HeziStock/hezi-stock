import { Card, CardContent } from "@/components/ui/card"
import { ListOrdered, Zap, UserX, TrendingUp, FileSpreadsheet, Brain } from "lucide-react"

const features = [
  {
    icon: ListOrdered,
    title: "Daily Ranked Ideas",
    description: "Get a short list, ranked 1-10, with clear reasoning for each entry.",
    gradient: "from-primary/20 to-primary/5",
    iconColor: "text-primary",
  },
  {
    icon: Zap,
    title: "Fast & Actionable",
    description: "Run a scan in seconds and export to CSV for quick execution.",
    gradient: "from-chart-3/20 to-chart-3/5",
    iconColor: "text-chart-3",
  },
  {
    icon: UserX,
    title: "No Signup",
    description: "Open the dashboard and run a report — nothing to set up.",
    gradient: "from-chart-2/20 to-chart-2/5",
    iconColor: "text-chart-2",
  },
  {
    icon: Brain,
    title: "AI-Powered Analysis",
    description: "Our AI evaluates market patterns, volume, and momentum signals.",
    gradient: "from-chart-5/20 to-chart-5/5",
    iconColor: "text-chart-5",
  },
  {
    icon: FileSpreadsheet,
    title: "CSV Export",
    description: "Download your results and integrate with your trading workflow.",
    gradient: "from-chart-4/20 to-chart-4/5",
    iconColor: "text-chart-4",
  },
  {
    icon: TrendingUp,
    title: "Market Movers",
    description: "Track gainers, losers, and trending stocks in real-time.",
    gradient: "from-primary/20 to-primary/5",
    iconColor: "text-primary",
  },
]

export function Features() {
  return (
    <section className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Section header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Everything you need to find
            <span className="text-primary"> winning trades</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Powerful AI tools designed to simplify your stock research and decision-making process.
          </p>
        </div>

        {/* Features grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="group relative overflow-hidden border-border bg-card hover:border-primary/50 transition-all duration-300"
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-300`} />
              <CardContent className="relative p-6">
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-xl bg-secondary mb-4 ${feature.iconColor}`}>
                  <feature.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
