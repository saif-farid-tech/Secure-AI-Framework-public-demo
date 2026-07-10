import { FilterStage as FilterStageType } from "@/types/pipeline";
import { AgentCard } from "./AgentCard";
import { cn } from "@/lib/utils";
import { Shield, ShieldCheck } from "lucide-react";

interface FilterStageProps {
  stage: FilterStageType;
  type: 'input' | 'output';
}

export function FilterStage({ stage, type }: FilterStageProps) {
  const Icon = type === 'input' ? Shield : ShieldCheck;
  const gradientDirection = type === 'input' ? 'from-left' : 'from-right';

  return (
    <div className="flex flex-col gap-4 animate-fade-in">
      <div className="flex items-center gap-3">
        <div className={cn(
          "w-10 h-10 rounded-xl flex items-center justify-center",
          "bg-gradient-to-br",
          type === 'input' 
            ? "from-primary/20 to-accent/20 border border-primary/30"
            : "from-success/20 to-primary/20 border border-success/30"
        )}>
          <Icon className={cn(
            "w-5 h-5",
            type === 'input' ? "text-primary" : "text-success"
          )} />
        </div>
        <div>
          <h3 className="font-semibold text-foreground">{stage.name}</h3>
          <p className="text-xs text-muted-foreground">
            {stage.agents.filter(a => a.status === 'complete').length} / {stage.agents.length} agents agreed
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {stage.agents.map((agent, index) => (
          <AgentCard key={agent.id} agent={agent} index={index} />
        ))}
      </div>
    </div>
  );
}
