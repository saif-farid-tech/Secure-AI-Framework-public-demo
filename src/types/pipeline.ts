export type AgentStatus = 'idle' | 'processing' | 'complete' | 'error';

export interface AgentOutput {
  id: string;
  name: string;
  status: AgentStatus;
  output: string;
  timestamp?: Date;
}

export interface FilterStage {
  name: string;
  agents: AgentOutput[];
  status: AgentStatus;
}

export interface PipelineState {
  inputPrompt: string;
  inputFilter: FilterStage;
  filteredPrompt: string;
  llmOutput: string;
  llmStatus: AgentStatus;
  outputFilter: FilterStage;
  finalOutput: string;
  isRunning: boolean;
}
