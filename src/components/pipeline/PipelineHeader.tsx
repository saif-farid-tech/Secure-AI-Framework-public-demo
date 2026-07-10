import { Shield, Swords } from "lucide-react";

export function PipelineHeader() {
  return (
    <header className="text-center mb-8 animate-fade-in">
      <div className="inline-flex items-center gap-3 mb-4">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-accent/40 to-accent/20 flex items-center justify-center border-2 crimson-border shadow-lg shadow-accent/20">
          <Shield className="w-6 h-6 text-steel-light" />
        </div>
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-accent/30 to-muted/30 flex items-center justify-center border border-primary/40 shadow-lg shadow-primary/10">
          <Swords className="w-6 h-6 text-steel-light" />
        </div>
      </div>
      
      <h1 className="text-3xl md:text-4xl font-bold mb-2">
        <span className="steel-text">SAIF</span>
        <span className="text-foreground"> Pipeline</span>
      </h1>
      
      <p className="text-muted-foreground max-w-lg mx-auto">
        Secure AI Framework — Visualize prompt filtering through 
        input guards, LLM processing, and output validation
      </p>
    </header>
  );
}
