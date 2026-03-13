"use client"

import { useState } from "react"
import {
  LayoutDashboard,
  TrendingUp,
  Briefcase,
  Brain,
  LineChart,
  Settings,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", active: true },
  { icon: TrendingUp, label: "Markets" },
  { icon: Briefcase, label: "Portfolio" },
  { icon: Brain, label: "AI Insights" },
  { icon: LineChart, label: "Analysis" },
]

const bottomItems = [
  { icon: Settings, label: "Settings" },
  { icon: HelpCircle, label: "Help" },
]

export function DashboardSidebar() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={cn(
        "flex flex-col border-r border-border bg-sidebar transition-all duration-300",
        collapsed ? "w-16" : "w-60"
      )}
    >
      <div className="flex flex-1 flex-col gap-1 p-3">
        {navItems.map((item) => (
          <Button
            key={item.label}
            variant={item.active ? "secondary" : "ghost"}
            className={cn(
              "justify-start gap-3",
              item.active && "bg-primary/10 text-primary hover:bg-primary/20",
              collapsed && "justify-center px-0"
            )}
          >
            <item.icon className="h-5 w-5 shrink-0" />
            {!collapsed && <span>{item.label}</span>}
          </Button>
        ))}
      </div>

      <div className="flex flex-col gap-1 border-t border-border p-3">
        {bottomItems.map((item) => (
          <Button
            key={item.label}
            variant="ghost"
            className={cn(
              "justify-start gap-3",
              collapsed && "justify-center px-0"
            )}
          >
            <item.icon className="h-5 w-5 shrink-0" />
            {!collapsed && <span>{item.label}</span>}
          </Button>
        ))}

        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          className="mt-2 self-end"
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </Button>
      </div>
    </aside>
  )
}
