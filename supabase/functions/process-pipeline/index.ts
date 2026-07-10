import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

// ============================================
// INPUT FILTER AGENTS - Add your custom logic here
// ============================================

async function runInputFilter1(prompt: string): Promise<{ passed: boolean; output: string }> {
  // TODO: Add your input filter logic
  // Example: Check for prompt injection attacks
  console.log("Running Input Filter 1: Prompt Injection Check");
  await new Promise(r => setTimeout(r, 300)); // Simulate processing
  return { passed: true, output: "No injection patterns detected" };
}

async function runInputFilter2(prompt: string): Promise<{ passed: boolean; output: string }> {
  // TODO: Add your input filter logic
  // Example: Content policy check
  console.log("Running Input Filter 2: Content Policy Check");
  await new Promise(r => setTimeout(r, 250));
  return { passed: true, output: "Content policy compliant" };
}

async function runInputFilter3(prompt: string): Promise<{ passed: boolean; output: string }> {
  // TODO: Add your input filter logic
  // Example: PII detection
  console.log("Running Input Filter 3: PII Detection");
  await new Promise(r => setTimeout(r, 200));
  return { passed: true, output: "No PII detected" };
}

async function runInputFilter4(prompt: string): Promise<{ passed: boolean; output: string }> {
  // TODO: Add your input filter logic
  // Example: Rate limiting / abuse detection
  console.log("Running Input Filter 4: Abuse Detection");
  await new Promise(r => setTimeout(r, 150));
  return { passed: true, output: "No abuse patterns detected" };
}

// ============================================
// LLM PROCESSING - Add your LLM endpoint here
// ============================================

async function callLLM(prompt: string): Promise<string> {
  // TODO: Replace with your actual LLM endpoint
  console.log("Calling LLM with filtered prompt");
  
  // Example: Call your custom LLM endpoint
  // const response = await fetch("YOUR_LLM_ENDPOINT", {
  //   method: "POST",
  //   headers: { 
  //     "Content-Type": "application/json",
  //     "Authorization": `Bearer ${Deno.env.get("YOUR_LLM_API_KEY")}`
  //   },
  //   body: JSON.stringify({ prompt })
  // });
  // const data = await response.json();
  // return data.response;

  // Placeholder response
  await new Promise(r => setTimeout(r, 500));
  return `LLM Response to: "${prompt.substring(0, 50)}..."

This is a placeholder response. Replace the callLLM function with your actual LLM endpoint integration.`;
}

// ============================================
// OUTPUT FILTER AGENTS - Add your custom logic here
// ============================================

async function runOutputFilter1(response: string): Promise<{ passed: boolean; output: string }> {
  // TODO: Add your output filter logic
  // Example: Hallucination detection
  console.log("Running Output Filter 1: Hallucination Check");
  await new Promise(r => setTimeout(r, 300));
  return { passed: true, output: "No hallucinations detected" };
}

async function runOutputFilter2(response: string): Promise<{ passed: boolean; output: string }> {
  // TODO: Add your output filter logic
  // Example: Factuality verification
  console.log("Running Output Filter 2: Factuality Check");
  await new Promise(r => setTimeout(r, 250));
  return { passed: true, output: "Response appears factual" };
}

async function runOutputFilter3(response: string): Promise<{ passed: boolean; output: string }> {
  // TODO: Add your output filter logic
  // Example: Toxicity check
  console.log("Running Output Filter 3: Toxicity Check");
  await new Promise(r => setTimeout(r, 200));
  return { passed: true, output: "No toxic content detected" };
}

async function runOutputFilter4(response: string): Promise<{ passed: boolean; output: string }> {
  // TODO: Add your output filter logic
  // Example: Format validation
  console.log("Running Output Filter 4: Format Validation");
  await new Promise(r => setTimeout(r, 150));
  return { passed: true, output: "Response format valid" };
}

// ============================================
// MAIN HANDLER
// ============================================

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { prompt } = await req.json();
    
    if (!prompt || typeof prompt !== 'string') {
      return new Response(
        JSON.stringify({ error: 'Invalid prompt provided' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    console.log("Processing pipeline for prompt:", prompt.substring(0, 100));

    // Run input filters sequentially (for proper visualization)
    const inputFilters = [
      { name: "Prompt Injection Check", fn: runInputFilter1 },
      { name: "Content Policy Check", fn: runInputFilter2 },
      { name: "PII Detection", fn: runInputFilter3 },
      { name: "Abuse Detection", fn: runInputFilter4 },
    ];

    const inputResults = [];
    for (const filter of inputFilters) {
      const result = await filter.fn(prompt);
      inputResults.push({ name: filter.name, ...result });
      
      if (!result.passed) {
        return new Response(
          JSON.stringify({ 
            error: `Input filter failed: ${filter.name}`,
            stage: 'input_filter',
            inputFilters: inputResults,
            outputFilters: [],
            llmOutput: null
          }),
          { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
    }

    // Call LLM
    const llmOutput = await callLLM(prompt);

    // Run output filters sequentially
    const outputFilters = [
      { name: "Hallucination Check", fn: runOutputFilter1 },
      { name: "Factuality Check", fn: runOutputFilter2 },
      { name: "Toxicity Check", fn: runOutputFilter3 },
      { name: "Format Validation", fn: runOutputFilter4 },
    ];

    const outputResults = [];
    for (const filter of outputFilters) {
      const result = await filter.fn(llmOutput);
      outputResults.push({ name: filter.name, ...result });
      
      if (!result.passed) {
        return new Response(
          JSON.stringify({ 
            error: `Output filter failed: ${filter.name}`,
            stage: 'output_filter',
            inputFilters: inputResults,
            outputFilters: outputResults,
            llmOutput
          }),
          { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
    }

    // Success - all filters passed
    return new Response(
      JSON.stringify({
        success: true,
        inputFilters: inputResults,
        llmOutput,
        outputFilters: outputResults
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );

  } catch (error) {
    console.error("Pipeline error:", error);
    return new Response(
      JSON.stringify({ error: error instanceof Error ? error.message : 'Unknown error' }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
});
