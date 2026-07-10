import { PipelineHeader } from "@/components/pipeline/PipelineHeader";
import { PromptInput } from "@/components/pipeline/PromptInput";
import { FilterStage } from "@/components/pipeline/FilterStage";
import { FilteredPromptBox } from "@/components/pipeline/FilteredPromptBox";
import { LLMStage } from "@/components/pipeline/LLMStage";
import { FlowConnector } from "@/components/pipeline/FlowConnector";
import { FinalOutput } from "@/components/pipeline/FinalOutput";
import { usePipeline } from "@/hooks/usePipeline";

const Index = () => {
  const { state, setInputPrompt, runPipeline, reset } = usePipeline();

  const isInputFilterActive = state.inputFilter.agents.some(
    (a) => a.status === "processing" || a.status === "complete"
  );
  const isLLMActive = state.llmStatus === "processing" || state.llmStatus === "complete";
  const isOutputFilterActive = state.outputFilter.agents.some(
    (a) => a.status === "processing" || a.status === "complete"
  );

  return (
    <div className="min-h-screen bg-background">
      {/* Background grid effect */}
      <div 
        className="fixed inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `
            linear-gradient(hsl(var(--primary) / 0.3) 1px, transparent 1px),
            linear-gradient(90deg, hsl(var(--primary) / 0.3) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px'
        }}
      />

      <div className="relative container max-w-5xl mx-auto px-4 py-8 md:py-12">
        <PipelineHeader />

        <div className="space-y-2">
          {/* Input Prompt */}
          <PromptInput
            value={state.inputPrompt}
            onChange={setInputPrompt}
            onSubmit={runPipeline}
            onReset={reset}
            isRunning={state.isRunning}
          />

          <FlowConnector 
            isActive={isInputFilterActive} 
            label="Input Filtering"
          />

          {/* Input Filter Stage */}
          <FilterStage stage={state.inputFilter} type="input" />

          {/* Filtered prompt shown after input agents complete */}
          <FilteredPromptBox prompt={state.filteredPrompt} />

          <FlowConnector
            isActive={isLLMActive}
            label="LLM Processing"
          />

          {/* LLM Stage */}
          <LLMStage output={state.llmOutput} status={state.llmStatus} />

          <FlowConnector 
            isActive={isOutputFilterActive} 
            label="Output Filtering"
          />

          {/* Output Filter Stage */}
          <FilterStage stage={state.outputFilter} type="output" />

          <FlowConnector 
            isActive={state.outputFilter.status === "complete"} 
            label="Complete"
          />

          {/* Final Output */}
          <FinalOutput
            output={state.outputFilter.status === "complete" ? state.finalOutput : ""}
            status={state.outputFilter.status}
          />
        </div>
      </div>
    </div>
  );
};

export default Index;
