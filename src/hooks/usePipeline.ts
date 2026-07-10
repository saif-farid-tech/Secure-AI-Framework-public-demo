import { useState, useCallback } from 'react';
import { PipelineState, AgentStatus } from '@/types/pipeline';

// Point this to your Python backend
const PYTHON_API_URL = 'http://127.0.0.1:5000'; // <--- Paste your URL here

const initialState: PipelineState = {
  inputPrompt: '',
  inputFilter: {
    name: 'Input Filters',
    status: 'idle',
    agents: [
      { id: 'if1', name: 'Agent 1 (principles 1-6)', status: 'idle', output: '' },
      { id: 'if2', name: 'Agent 2 (principles 7-12)', status: 'idle', output: '' },
    ],
  },
  filteredPrompt: '',
  llmOutput: '',
  llmStatus: 'idle',
  outputFilter: {
    name: 'Output Filters',
    status: 'idle',
    agents: [
      { id: 'of1', name: 'Agent 1 (principles 1-6)', status: 'idle', output: '' },
      { id: 'of2', name: 'Agent 2 (principles 7-12)', status: 'idle', output: '' },
    ],
  },
  finalOutput: '',
  isRunning: false,
};

export function usePipeline() {
  const [state, setState] = useState<PipelineState>(initialState);

  const setInputPrompt = useCallback((prompt: string) => {
    setState(prev => ({ ...prev, inputPrompt: prompt }));
  }, []);

  const updateAgentStatus = useCallback((
    filterType: 'inputFilter' | 'outputFilter',
    agentId: string,
    status: AgentStatus,
    output?: string
  ) => {
    setState(prev => ({
      ...prev,
      [filterType]: {
        ...prev[filterType],
        agents: prev[filterType].agents.map(agent =>
          agent.id === agentId
            ? { ...agent, status, output: output ?? agent.output }
            : agent
        ),
      },
    }));
  }, []);

  const runPipeline = useCallback(async () => {
    if (!state.inputPrompt.trim()) return;

    const agentIds = {
      input: ['if1', 'if2'],
      output: ['of1', 'of2'],
    };

    // Reset and start
    setState(prev => ({
      ...initialState,
      inputPrompt: prev.inputPrompt,
      isRunning: true,
      inputFilter: {
        ...initialState.inputFilter,
        agents: initialState.inputFilter.agents.map(a => ({ ...a, status: 'processing' as AgentStatus })),
      },
    }));

    try {
      const response = await fetch(`${PYTHON_API_URL}/process-pipeline`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: state.inputPrompt })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No response body');

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Parse complete SSE messages from the buffer
        const lines = buffer.split('\n');
        buffer = '';
        let eventType = '';

        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];

          if (line.startsWith('event: ')) {
            eventType = line.slice(7).trim();
          } else if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));

            if (eventType === 'input_agent') {
              const agentId = agentIds.input[data.index];
              updateAgentStatus(
                'inputFilter',
                agentId,
                data.passed ? 'complete' : 'error',
                data.output
              );
            } else if (eventType === 'filtered_prompt') {
              setState(prev => ({ ...prev, filteredPrompt: data.prompt }));
            } else if (eventType === 'llm_output') {
              setState(prev => ({
                ...prev,
                llmOutput: data.output,
                llmStatus: 'complete',
                // Set output agents to processing now that LLM is done
                outputFilter: {
                  ...prev.outputFilter,
                  agents: prev.outputFilter.agents.map(a => ({ ...a, status: 'processing' as AgentStatus })),
                },
              }));
            } else if (eventType === 'output_agent') {
              const agentId = agentIds.output[data.index];
              updateAgentStatus(
                'outputFilter',
                agentId,
                data.passed ? 'complete' : 'error',
                data.output
              );
            } else if (eventType === 'final_output') {
              setState(prev => ({
                ...prev,
                outputFilter: { ...prev.outputFilter, status: 'complete' },
                finalOutput: data.output,
              }));
            } else if (eventType === 'error') {
              console.error('Pipeline error:', data.error);
              for (const id of agentIds.input) {
                updateAgentStatus('inputFilter', id, 'error', data.error);
              }
            } else if (eventType === 'done') {
              // Pipeline finished
            }

            eventType = '';
          } else if (line === '') {
            // Empty line is the SSE message delimiter, ignore
          } else {
            // Incomplete line, put back in buffer
            buffer = lines.slice(i).join('\n');
            break;
          }
        }
      }

    } catch (err) {
      console.error('Pipeline execution error:', err);
    } finally {
      setState(prev => ({ ...prev, isRunning: false }));
    }
  }, [state.inputPrompt, updateAgentStatus]);

  const reset = useCallback(() => {
    setState(initialState);
  }, []);

  return {
    state,
    setInputPrompt,
    runPipeline,
    reset,
  };
}
