import { cn } from "@/lib/utils";
import { ChevronRight, ArrowRight } from "lucide-react";

interface FlowConnectorProps {
  isActive?: boolean;
  direction?: 'horizontal' | 'vertical';
  label?: string;
}

export function FlowConnector({ 
  isActive = false, 
  direction = 'vertical',
  label 
}: FlowConnectorProps) {
  if (direction === 'horizontal') {
    return (
      <div className="flex items-center justify-center px-2">
        <div className={cn(
          "flex items-center gap-1",
          isActive ? "text-primary" : "text-muted-foreground/50"
        )}>
          <div className={cn(
            "h-0.5 w-8",
            isActive ? "bg-gradient-to-r from-primary/50 to-primary flow-animation" : "bg-border"
          )} />
          <ArrowRight className={cn(
            "w-4 h-4",
            isActive && "animate-pulse-subtle"
          )} />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center py-4">
      <div className={cn(
        "w-0.5 h-8 rounded-full",
        isActive ? "bg-gradient-to-b from-primary/50 to-primary" : "bg-border"
      )} />
      {label && (
        <div className={cn(
          "my-2 px-3 py-1 rounded-full text-xs font-medium",
          isActive ? "bg-primary/10 text-primary border border-primary/30" : "bg-muted text-muted-foreground"
        )}>
          {label}
        </div>
      )}
      <div className={cn(
        "w-0.5 h-8 rounded-full",
        isActive ? "bg-gradient-to-b from-primary to-primary/50" : "bg-border"
      )} />
      <ChevronRight className={cn(
        "w-5 h-5 rotate-90",
        isActive ? "text-primary animate-pulse-subtle" : "text-muted-foreground/50"
      )} />
    </div>
  );
}
