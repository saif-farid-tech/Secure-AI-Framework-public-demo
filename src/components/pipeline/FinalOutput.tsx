import { AgentStatus } from "@/types/pipeline";
import { cn } from "@/lib/utils";
import { FileOutput, Copy, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface FinalOutputProps {
  output: string;
  status: AgentStatus;
}

export function FinalOutput({ output, status }: FinalOutputProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={cn(
      "glass-card p-6 animate-fade-in",
      status === 'complete' && "border-success/30"
    )}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={cn(
            "w-10 h-10 rounded-xl flex items-center justify-center",
            "bg-gradient-to-br from-success/20 to-primary/20",
            "border border-success/30"
          )}>
            <FileOutput className="w-5 h-5 text-success" />
          </div>
          <div>
            <h3 className="font-semibold text-lg text-foreground">Final Output</h3>
            <p className="text-sm text-muted-foreground">
              Filtered and processed result
            </p>
          </div>
        </div>

        {output && (
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className="text-muted-foreground hover:text-foreground"
          >
            {copied ? (
              <>
                <CheckCircle2 className="w-4 h-4 mr-2 text-success" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="w-4 h-4 mr-2" />
                Copy
              </>
            )}
          </Button>
        )}
      </div>

      <div className={cn(
        "bg-background/50 rounded-lg p-4 border min-h-[100px] max-h-[200px] overflow-y-auto scrollbar-thin",
        status === 'complete' ? "border-success/30" : "border-border/50"
      )}>
        {output ? (
          <pre className="font-mono text-sm text-foreground whitespace-pre-wrap break-words">
            {output}
          </pre>
        ) : (
          <span className="text-sm text-muted-foreground/50 italic">
            Waiting for pipeline to complete...
          </span>
        )}
      </div>
    </div>
  );
}
