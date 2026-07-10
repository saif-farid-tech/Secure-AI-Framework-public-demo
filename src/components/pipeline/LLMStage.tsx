import { AgentStatus } from "@/types/pipeline";
import { cn } from "@/lib/utils";
import { Brain, Loader2, CheckCircle2, AlertCircle } from "lucide-react";

interface LLMStageProps {
  output: string;
  status: AgentStatus;
}

export function LLMStage({ output, status }: LLMStageProps) {
  return (
    <div className="glass-card p-6 animate-fade-in">
      <div className="flex items-center gap-3 mb-4">
        <div className={cn(
          "w-12 h-12 rounded-xl flex items-center justify-center",
          "bg-gradient-to-br from-primary/30 to-accent/30",
          "border-2",
          status === 'processing' ? "border-warning animate-pulse" :
          status === 'complete' ? "border-success" :
          status === 'error' ? "border-destructive" :
          "border-primary/50"
        )}>
          {status === 'processing' ? (
            <Loader2 className="w-6 h-6 text-warning animate-spin" />
          ) : status === 'complete' ? (
            <CheckCircle2 className="w-6 h-6 text-success" />
          ) : status === 'error' ? (
            <AlertCircle className="w-6 h-6 text-destructive" />
          ) : (
            <Brain className="w-6 h-6 text-primary" />
          )}
        </div>
        <div>
          <h3 className="font-semibold text-lg text-foreground flex items-center gap-2">
            LLM Processing
            {status === 'processing' && (
              <span className="text-xs text-warning bg-warning/10 px-2 py-0.5 rounded-full">
                Generating...
              </span>
            )}
          </h3>
          <p className="text-sm text-muted-foreground">
            Large Language Model Output
          </p>
        </div>
      </div>

      <div className="bg-background/50 rounded-lg p-4 border border-border/50 min-h-[120px] max-h-[200px] overflow-y-auto scrollbar-thin">
        {output ? (
          <pre className="font-mono text-sm text-foreground/90 whitespace-pre-wrap break-words">
            {output}
          </pre>
        ) : (
          <span className="text-sm text-muted-foreground/50 italic">
            Waiting for filtered prompt...
          </span>
        )}
      </div>
    </div>
  );
}
