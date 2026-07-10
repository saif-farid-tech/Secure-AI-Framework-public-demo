import { cn } from "@/lib/utils";
import { AgentOutput, AgentStatus } from "@/types/pipeline";
import { Bot, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface AgentCardProps {
  agent: AgentOutput;
  index: number;
}

const statusConfig: Record<AgentStatus, { icon: React.ReactNode; className: string }> = {
  idle: {
    icon: <Bot className="w-4 h-4" />,
    className: "status-idle",
  },
  processing: {
    icon: <Loader2 className="w-4 h-4 animate-spin" />,
    className: "status-processing",
  },
  complete: {
    icon: <CheckCircle2 className="w-4 h-4" />,
    className: "status-complete",
  },
  error: {
    icon: <AlertCircle className="w-4 h-4" />,
    className: "status-error",
  },
};

export function AgentCard({ agent, index }: AgentCardProps) {
  const config = statusConfig[agent.status];

  // Helper to extract harm level from the formatted output
  // Updated regex to capture anything until the end of the line
  const getHarmLevel = (output: string) => {
    const match = output.match(/\*\*Harm Level:\*\*\s*([^\n]+)/i);
    return match ? match[1].trim() : null;
  };

  const harmLevel = getHarmLevel(agent.output);
  
  // Determine display label: use harmLevel if available and status is not idle/processing
  const displayLabel = (agent.status === 'complete' || agent.status === 'error') && harmLevel 
    ? harmLevel 
    : agent.status;

  // Remove the Harm Level line from the display output
  // Regex matches: **Harm Level:** + any chars until newline + optional following newlines
  const displayOutput = agent.output
    ? agent.output.replace(/\*\*Harm Level:\*\*[^\n]*\n*/i, '').trim()
    : '';

  return (
    <div
      className={cn(
        "agent-card glow-border animate-fade-in",
        agent.status === 'processing' && "pulse-glow"
      )}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center border border-primary/30">
            <span className="text-primary font-mono text-sm font-semibold">
              {index + 1}
            </span>
          </div>
          <span className="font-medium text-foreground">{agent.name}</span>
        </div>
        <div
          className={cn(
            "flex items-center gap-1.5 px-2 py-1 rounded-full text-xs border",
            config.className
          )}
        >
          {config.icon}
          <span className="capitalize">{displayLabel}</span>
        </div>
      </div>

      <div className="bg-background/50 rounded-md p-3 border border-border/50 min-h-[80px] max-h-[120px] overflow-y-auto scrollbar-thin">
        {agent.output ? (
          <div className="prose prose-sm prose-invert max-w-none text-xs text-muted-foreground">
            <ReactMarkdown>{displayOutput}</ReactMarkdown>
          </div>
        ) : (
          <span className="text-xs text-muted-foreground/50 italic">
            Waiting for input...
          </span>
        )}
      </div>
    </div>
  );
}
