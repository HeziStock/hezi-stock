import { Button } from "@/components/ui/button"
import { ArrowRight, Mail } from "lucide-react"

export function CTA() {
  return (
    <section className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary/20 via-card to-chart-2/10 border border-border p-8 sm:p-12 md:p-16">
          {/* Background decoration */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-chart-2/10 rounded-full blur-3xl" />
          
          <div className="relative z-10 text-center">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 text-balance">
              Ready to find your next
              <span className="text-primary"> winning trade?</span>
            </h2>
            <p className="text-muted-foreground text-lg max-w-xl mx-auto mb-8">
              Start scanning the market with AI-powered insights. No credit card, no signup - just results.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button size="lg" className="group px-8 py-6 text-lg bg-primary hover:bg-primary/90">
                Open Dashboard
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button size="lg" variant="outline" className="px-8 py-6 text-lg border-border hover:bg-secondary">
                <Mail className="mr-2 w-5 h-5" />
                Request Demo
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
