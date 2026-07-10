import { cn } from "@/lib/utils";
import { FileText } from "lucide-react";

interface FilteredPromptBoxProps {
  prompt: string;
}

export function FilteredPromptBox({ prompt }: FilteredPromptBoxProps) {
  if (!prompt) return null;

  return (
    <div className={cn("glass-card p-4 animate-fade-in border border-primary/20")}>
      <div className="flex items-center gap-2 mb-3">
        <div className="w-7 h-7 rounded-lg flex items-center justify-center bg-primary/10 border border-primary/20">
          <FileText className="w-4 h-4 text-primary" />
        </div>
        <div>
          <h4 className="text-sm font-semibold text-foreground">Filtered Prompt</h4>
          <p className="text-xs text-muted-foreground">Sanitised input passed to the LLM</p>
        </div>
      </div>
      <div className="bg-background/50 rounded-lg p-3 border border-border/50 max-h-[150px] overflow-y-auto scrollbar-thin">
        <pre className="font-mono text-sm text-foreground/90 whitespace-pre-wrap break-words">
          {prompt}
        </pre>
      </div>
    </div>
  );
}
