import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Play, RotateCcw, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface PromptInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  onReset: () => void;
  isRunning: boolean;
}

export function PromptInput({ value, onChange, onSubmit, onReset, isRunning }: PromptInputProps) {
  return (
    <div className="glass-card p-6 animate-fade-in">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center border border-primary/30">
          <Sparkles className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h2 className="font-semibold text-lg text-foreground">Input Prompt</h2>
          <p className="text-sm text-muted-foreground">Enter your prompt to process through the filter pipeline</p>
        </div>
      </div>

      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Enter your prompt here..."
        className={cn(
          "min-h-[120px] bg-background/50 border-border/50 font-mono text-sm",
          "focus:border-primary/50 focus:ring-primary/20",
          "placeholder:text-muted-foreground/50"
        )}
        disabled={isRunning}
      />

      <div className="flex gap-3 mt-4">
        <Button
          onClick={onSubmit}
          disabled={!value.trim() || isRunning}
          className={cn(
            "flex-1 bg-gradient-to-r from-primary to-accent",
            "hover:from-primary/90 hover:to-accent/90",
            "text-primary-foreground font-medium",
            "shadow-lg shadow-primary/20"
          )}
        >
          {isRunning ? (
            <>
              <Play className="w-4 h-4 mr-2 animate-pulse" />
              Processing...
            </>
          ) : (
            <>
              <Play className="w-4 h-4 mr-2" />
              Run Pipeline
            </>
          )}
        </Button>
        
        <Button
          variant="outline"
          onClick={onReset}
          disabled={isRunning}
          className="border-border/50 hover:bg-muted hover:border-muted-foreground/30"
        >
          <RotateCcw className="w-4 h-4 mr-2" />
          Reset
        </Button>
      </div>
    </div>
  );
}
