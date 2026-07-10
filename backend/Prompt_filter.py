import os
from typing import TypedDict, Annotated, List, Dict, Optional, Tuple
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# Removed: Alias the imports to ensure they are the correct ones from langchain_core
# Removed: from langchain_core.messages import HumanMessage as LcHumanMessage, SystemMessage as LcSystemMessage
import operator
from pathlib import Path
import networkx as nx  # For actual graphs
import re  # For extracting entities

# Try to import Docling for PDF processing
try:
    from docling.document_converter import DocumentConverter
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    print("Warning: Docling not installed. PDF support disabled. Install with: pip install docling")

"""
UAE Charter-Aligned Multi-Agent System Prompts

System prompts for 4 agents based on the UAE Charter for the Development
and Use of Artificial Intelligence (July 2024)
"""

# ==================================================================================================
# AGENT 1: Human-Machine Ties, Safety, Algorithmic Bias, Data Privacy, Transparency, Human Oversight
# ==================================================================================================

AGENT1_ASSESSMENT_PROMPT = """You are a specialized AI safety, privacy, transparency and human oversight expert focused on evaluating prompts according to the UAE Charter for AI Development and Use.

Your specific areas of expertise are:

1. STRENGTHENING HUMAN-MACHINE TIES:
   - Evaluate if the prompt promotes harmonious and beneficial relationships between AI and humans
   - Check if human well-being and progress are prioritized
   - Identify prompts that might undermine human dignity or autonomy

2. SAFETY:
   - Assess if the prompt could lead to unsafe AI system behavior
   - Identify requests that could pose risks to individuals or society
   - Flag prompts that encourage bypassing safety standards or removing safety systems

3. ALGORITHMIC BIAS & FAIRNESS:
   - Detect bias, discrimination, or exclusionary language
   - Identify prompts that could lead to unfair treatment of any community members
   - Flag requests that don't respect individual differences or diversity
   - Check for prompts that could result in unequal access to technology or its benefits

4. DATA PRIVACY:
   - Identify any personal information, personally identifiable information (PII), or sensitive data
   - Detect doxxing attempts or privacy violations
   - Check if the prompt respects community members' privacy rights
   - Ensure data handling aligns with privacy-first principles

5. TRANSPARENCY:
   - Assess if the prompt requests hidden, deceptive, or opaque operations
   - Check if the prompt undermines understanding of how AI systems work
   - Identify requests that reduce accountability or explainability
   - Flag prompts that obscure AI decision-making processes

6. HUMAN OVERSIGHT:
   - Evaluate if the prompt attempts to remove or bypass human judgment
   - Check if the prompt undermines human oversight of AI systems
   - Identify requests that don't align with ethical values and social standards
   - Ensure human judgment remains irreplaceable in critical decisions

Classify the harm level as: "safe", "mild", "moderate", or "severe"

Provide a clear assessment of what issues you found related to human-machine relationship, safety, fairness concerns, privacy, transparency, or human oversight."""

AGENT1_TRANSFORMATION_PROMPT = """You are a specialized AI safety, privacy, transparency and human oversight expert who transforms prompts to align with the UAE Charter for AI Development and Use.

Your transformation must ensure:

1. STRENGTHENING HUMAN-MACHINE TIES:
   - Reframe prompts to enhance harmonious human-AI collaboration
   - Ensure human well-being and progress are central
   - Preserve human dignity and autonomy

2. SAFETY:
   - Remove any unsafe requests or risk-promoting elements
   - Redirect toward prompts that comply with highest safety standards
   - Ensure the prompt won't lead to harmful system behavior

3. ALGORITHMIC BIAS & FAIRNESS:
   - Eliminate discriminatory, biased, or exclusionary language
   - Ensure fairness and equity for all community members
   - Make technology inclusive and accessible to everyone
   - Respect diversity and individual differences
   - Ensure equal technological benefits without exclusion or discrimination

4. DATA PRIVACY:
   - Remove all personal information and PII
   - Eliminate any privacy violations or doxxing attempts
   - Redirect toward privacy-respecting alternatives
   - Ensure community members' privacy remains a top priority
   - Promote responsible data handling practices

5. TRANSPARENCY:
   - Promote clear understanding of AI operations and decision-making
   - Ensure the request builds trust through transparency
   - Enhance responsibility and accountability
   - Make AI systems' processes understandable and explainable

6. HUMAN OVERSIGHT:
   - Emphasize the irreplaceable value of human judgment
   - Ensure prompts maintain human oversight over AI systems
   - Align requests with ethical values and social standards
   - Keep humans in control of critical decisions
   - Ensure AI assists humans rather than replacing human judgment

Transform the prompt to promote responsible, safe, and fair AI development that benefits all of society, while ensuring privacy, transparency, and appropriate human oversight in AI systems."""

# =============================================================================================================================
# AGENT 2: Governance & Accountability, Tech Excellence, Human Commitment, Peaceful Coexistence, AI Awareness, Legal Compliance
# =============================================================================================================================

AGENT2_ASSESSMENT_PROMPT = """You are a specialized governance, accountability, technology, ethics, and legal and social responsibility expert focused on evaluating prompts according to the UAE Charter for AI Development and Use.

Your specific areas of expertise are:

1. GOVERNANCE AND ACCOUNTABILITY:
   - Assess if the prompt undermines responsible AI governance
   - Check if accountability mechanisms would be compromised
   - Identify requests that promote unethical or non-transparent AI use
   - Ensure the prompt aligns with principles of responsible technology governance

2. TECHNOLOGICAL EXCELLENCE:
   - Evaluate if the prompt promotes innovation and excellence
   - Check if the request aligns with ethical digital, technological, and scientific advancement
   - Identify prompts that undermine quality of life or sustainable progress
   - Assess if the prompt contributes to solving complex challenges constructively

3. HUMAN COMMITMENT:
   - Determine if the prompt serves the public good
   - Check if human well-being and fundamental rights are protected
   - Identify requests that don't place human values at the heart of technology
   - Ensure the prompt promotes positive societal impact

4. PEACEFUL COEXISTENCE WITH AI:
   - Assess if the prompt promotes technology that enhances community well-being
   - Check if the request compromises human security or fundamental rights
   - Identify prompts that create conflict rather than harmony, using AI systems
   - Ensure technology serves progress without threatening security

5. PROMOTING AI AWARENESS FOR AN INCLUSIVE FUTURE:
   - Evaluate if the prompt promotes equitable access to AI technology
   - Identify if any segments of society may be harmed, from the request
   - Identify exclusionary elements that limit AI's advantages to certain groups
   - Ensure the prompt contributes to inclusive AI advancement
   - Assess if the request promotes understanding and awareness of AI

6. COMMITMENT TO TREATIES AND APPLICABLE LAWS:
   - Identify violations of international treaties or local laws
   - Check compliance with legal frameworks governing AI development and use
   - Flag requests that circumvent legal requirements
   - Ensure the prompt respects both international and UAE legal standards

Classify the harm level as: "safe", "mild", "moderate", or "severe"

Provide a clear assessment of what issues you found related to governance, accountability, technological excellence, human-centered values, peaceful coexistence, inclusivity, or legal compliance."""

AGENT2_TRANSFORMATION_PROMPT = """You are a specialized governance, accountability, technology, ethics, and legal and social responsibility expert who transforms prompts to align with the UAE Charter for AI Development and Use.

Your transformation must ensure:

1. GOVERNANCE AND ACCOUNTABILITY:
   - Promote responsible and proactive AI governance
   - Ensure accountability in AI development and use
   - Direct toward ethical and transparent technology practices
   - Build trust through proper governance mechanisms

2. TECHNOLOGICAL EXCELLENCE:
   - Redirect toward innovation that drives progress, ethically
   - Promote ethical digital, technological, and scientific excellence
   - Ensure the request enhances competitiveness and quality of life
   - Focus on innovative solutions to complex challenges
   - Contribute to sustainable progress that benefits society as a whole
   - Make AI a beacon of innovation reflecting UAE's vision

3. HUMAN COMMITMENT:
   - Ensure the technology serves the public good
   - Protect human well-being and fundamental rights
   - Place human values at the heart of technological innovation
   - Create positive impact on society
   - Emphasize that AI development must enhance human flourishing

4. PEACEFUL COEXISTENCE WITH AI:
   - Promote technology that enhances community well-being and progress
   - Ensure human security and fundamental rights are protected
   - Create harmony between humans and AI systems
   - Redirect from conflict to cooperation, using technology
   - Ensure AI advances society without compromising safety

5. PROMOTING AI AWARENESS FOR AN INCLUSIVE FUTURE:
   - Create inclusive opportunities for all segments of society
   - Ensure equitable access to AI technology and its benefits
   - Remove exclusionary elements
   - Promote understanding and awareness of AI capabilities and limitations
   - Guarantee that everyone can benefit from AI advancements
   - Foster an inclusive future where AI serves all community members

6. COMMITMENT TO TREATIES AND APPLICABLE LAWS:
   - Ensure full compliance with international treaties
   - Align with local UAE laws and regulations
   - Redirect illegal or non-compliant requests toward lawful alternatives
   - Respect both international and domestic legal frameworks
   - Promote responsible AI development within established legal boundaries

Transform the prompt to promote responsible governance, accountability, technological excellence, genuine human commitment in AI development, peaceful coexistence with AI, inclusive access to technology, and full legal compliance."""

# ============================================================================
# KNOWLEDGE GRAPH BUILDER WITH DOCLING PDF SUPPORT
# ============================================================================

class TrueKnowledgeGraph:
    """
    TRUE Knowledge Graph using NetworkX.

    Structure:
    - Nodes: Entities (concepts, patterns, principles)
    - Edges: Relationships between entities
    - Embeddings: For semantic search over graph nodes

    This is GraphRAG, not vector RAG!
    We will use the relationships, to make the LLM make more informed decisions.
    """

    def __init__(
        self,
        agent_name: str,
        knowledge_docs_path: Optional[str] = None, #The file path for the agent.
        api_key: str = None
    ):
        """
        Initialize TRUE knowledge graph.

        NEW COMPONENTS vs Vector RAG:
        - self.graph: NetworkX graph with nodes and edges
        - self.node_embeddings: Embeddings for graph nodes (semantic search)
        - self.entity_relationships: Explicit relationships
        """
        self.agent_name = agent_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        # NEW: NetworkX graph (this is what makes it GraphRAG!)
        self.graph = nx.Graph()

        # NEW: Store node embeddings (for semantic search over nodes)
        self.embeddings = OpenAIEmbeddings(api_key=self.api_key)
        self.node_embeddings = {}  # {node_id: embedding_vector}

        # NEW: Entity types and relationships
        self.entity_types = {}  # {node_id: type}
        self.relationships = []  # [(source, target, relationship_type)]

        # Initialize Docling converter if available
        self.pdf_converter = None
        if DOCLING_AVAILABLE:
            try:
                self.pdf_converter = DocumentConverter()
                print(f"\n[{self.agent_name}] Docling PDF converter initialized")
            except Exception as e:
                print(f"\n[{self.agent_name}] Warning: Could not initialize Docling: {e}")

        # Load knowledge if path provided
        if knowledge_docs_path and os.path.exists(knowledge_docs_path):
            self.load_knowledge(knowledge_docs_path)

    def _load_pdf_with_docling(self, file_path: Path) -> Optional[str]:
        """Load PDF using IBM Docling."""
        if not self.pdf_converter: #If Docling was not loaded
            return None

        try:
            result = self.pdf_converter.convert(str(file_path)) #Convert PDF using Docling
            #Extract text content, into the content variable
            #Docling returns a Document object with a markdown export (basically LLM-readable format)
            content = result.document.export_to_markdown() #clean Markdown from PDF
            return content
        except Exception as e:
            print(f"[{self.agent_name}] Warning: Docling failed for {file_path}: {e}")
            return None

    def _extract_entities_and_relationships(self, content: str, source_file: str) -> Tuple[List[Dict], List[Tuple]]:
        """
        Extract entities and relationships from text to build graph.

        This is the KEY difference from vector RAG!
        We extract STRUCTURED information (entities + relationships) not just chunks.

        Returns:
            entities: List of {id, text, type, source}
            relationships: List of (source_entity, target_entity, relation_type)
        """
        entities = []
        relationships = []

        # Entity patterns to extract
        """Use the most common entity types in those patterns,
        based on the documents in the RAG database, to make the graph more meaningful.
        After, a graph is still structured data."""
        patterns = {
            'fines_pattern': r'(?:Fine|fine):\s*(.+?)(?:\n|$)',
            'rights_pattern': r'(?:Right|right):\s*(.+?)(?:\n|$)',
            'violation_pattern': r'(?:Violation|violation)\s*(\d+)[:\s]+(.+?)(?:\n|$)',
            'compliance_pattern': r'(?:Compliance|compliance):\s*(.+?)(?:\n|$)',
            'policy_pattern': r'(?:Policy|policy):\s*(.+?)(?:\n|$)',
            'authority_pattern': r'(?:Authority|authority):\s*(.+?)(?:\n|$)',
        }

        entity_id_counter = 0
        entity_map = {}  # text -> entity_id, used to find entity IDs when extracting relationships

        # Extract entities from predefined patterns
        for entity_type, pattern in patterns.items():
            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                entity_text = match.group(1).strip()
                if len(entity_text) < 10: #Because short text may be irrelavant
                    continue

                if entity_text.lower() not in entity_map: # to ensure uniqueness
                    entity_id = f"{source_file}_{entity_type}_{entity_id_counter}"
                    entity_id_counter += 1
                    entity = {
                        'id': entity_id,
                        'text': entity_text,
                        'type': entity_type,
                        'source': source_file
                    }
                    entities.append(entity)
                    entity_map[entity_text.lower()] = entity_id

        # Extract relationships
        """Write those regex patterns, based off the most common relationships
        inbetween entities, in the documents in the RAG database."""
        relationship_patterns = [
            (r'(.+?)\s*→\s*(.+?)(?:\n|$)', 'leads_to'),
            (r'(.+?)\s+controls\s+(.+?)(?:\n|$)', 'controls'),
            (r'(.+?)\s+requires\s+(.+?)(?:\n|$)', 'requires'),
            (r'(.+?)\s+violates\s+(.+?)(?:\n|$)', 'violates'),
        ]

        for pattern, relation_type in relationship_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
            #The REGEX parentheses `()` create capture groups, for the source and target
            for match in matches:
                source_text = match.group(1).strip().lower()
                target_text = match.group(2).strip().lower()

                # Ensure source entity exists or create it

                #This helps to ensure that even if some entities were not recognized in the REGEX patterns.
                #Then at least, we get to map their relations.
                source_id = entity_map.get(source_text)
                if not source_id:
                    entity_id = f"{source_file}_concept_{entity_id_counter}"
                    entity_id_counter += 1
                    new_entity = {
                        'id': entity_id,
                        'text': source_text, # Use the lowercased text for consistency
                        'type': 'concept',
                        'source': source_file
                    }
                    entities.append(new_entity)
                    entity_map[source_text] = entity_id
                    source_id = entity_id

                # Ensure target entity exists or create it
                #Same idea as before, with creating a 'concept' source entity
                target_id = entity_map.get(target_text)
                if not target_id:
                    entity_id = f"{source_file}_concept_{entity_id_counter}"
                    entity_id_counter += 1
                    new_entity = {
                        'id': entity_id,
                        'text': target_text, # Use the lowercased text for consistency
                        'type': 'concept',
                        'source': source_file
                    }
                    entities.append(new_entity)
                    entity_map[target_text] = entity_id
                    target_id = entity_id

                # Add relationship if both source and target IDs are valid
                if source_id and target_id:
                    relationships.append((source_id, target_id, relation_type))

        return entities, relationships

    def load_knowledge(self, docs_path: str):
        """
        NEW: Load documents and build GRAPH structure (not just vectors).

        Key differences from vector RAG:
        1. Extract entities and relationships (graph structure)
        2. Build NetworkX graph with nodes and edges
        3. Create embeddings for NODES (not document chunks)
        """
        path = Path(docs_path)
        supported_extensions = ['.txt', '.md', '.json', '.pdf']

        all_entities = []
        all_relationships = []

        # Load all files and extract entities/relationships
        for file_path in path.glob("**/*"):
            if file_path.suffix not in supported_extensions: #Skip any unsupported file types
                continue

            try:
                content = None

                # Handle PDF files with Docling
                if file_path.suffix == '.pdf':
                    if DOCLING_AVAILABLE and self.pdf_converter:
                        print(f"[{self.agent_name}] Processing PDF: {file_path.name}")
                        content = self._load_pdf_with_docling(file_path)
                        if not content: #This is if the content is empty (nothing was extracted from the PDF file)
                            continue
                    else: #This is if Docling was not loaded
                        continue

                # Handle text files
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                if content:
                    # Now, Extract entities and relationships
                    entities, relationships = self._extract_entities_and_relationships(
                        #This will use the previous fucnction to extract the entities and relationships
                        content,
                        file_path.name
                    )
                    all_entities.extend(entities)
                    all_relationships.extend(relationships)

                    print(f"\n[{self.agent_name}] Loaded: {file_path.name} "
                          f"({len(entities)} entities, {len(relationships)} relationships)")

            except Exception as e:
                print(f"[{self.agent_name}] Warning: Could not load {file_path}: {e}")

        if not all_entities: #If no entities were found
            print(f"[{self.agent_name}] Warning: No entities found in {docs_path}")
            return

        # Build graph structure
        self._build_graph(all_entities, all_relationships)

        # Create embeddings for nodes
        self._embed_nodes()

        #Prints stats for the built knowledge graph
        print(f"[{self.agent_name}] Built knowledge graph: "
              f"{self.graph.number_of_nodes()} nodes, "
              f"{self.graph.number_of_edges()} edges")

    def _build_graph(self, entities: List[Dict], relationships: List[Tuple]):
        """
        NEW: Build NetworkX graph from entities and relationships.

        This creates the actual GRAPH structure:
        - Add nodes for each entity
        - Add edges for each relationship
        - Store entity metadata as node attributes
        """
        # Add nodes
        for entity in entities:
            self.graph.add_node(
                entity['id'],
                text=entity['text'],
                type=entity['type'],
                source=entity['source']
            )
            self.entity_types[entity['id']] = entity['type']

        # Add edges
        for source, target, relation_type in relationships:
            if self.graph.has_node(source) and self.graph.has_node(target):
                self.graph.add_edge(source, target, relation=relation_type)
                self.relationships.append((source, target, relation_type))

    def _embed_nodes(self):
        """
        Create embeddings for graph NODES (not document chunks).

        Key difference from vector RAG:
        - Vector RAG: Embeddings of document chunks
        - GraphRAG: Embeddings of entity nodes

        We embed the entity text for semantic search over the graph.
        """
        if self.graph.number_of_nodes() == 0: #if the graph is empty
            return

        # Get all node texts
        node_texts = {}
        for node in self.graph.nodes():
            node_data = self.graph.nodes[node]
            node_texts[node] = node_data.get('text', '') # '' avoids a KeyError if the node has no 'text' attribute.

        # Create embeddings
        texts = list(node_texts.values())
        if texts:
            embeddings = self.embeddings.embed_documents(texts) #uses the embedding model from OpenAI, as from __init__

            for node, embedding in zip(node_texts.keys(), embeddings):
                self.node_embeddings[node] = embedding #fills the empty dicitionary from __init__.
                #They are in the same order, as we created embeddings from texts, from node_texts

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def retrieve_relevant_subgraph(self, query: str, k: int = 5) -> str:
        """
        NEW: Retrieve relevant SUBGRAPH (not just similar chunks).

        GraphRAG retrieval process:
        1. Embed the query
        2. Find k most similar NODES (not chunks)
        3. Extract SUBGRAPH around those nodes (includes connected nodes)
        4. Include relationship information

        This is fundamentally different from vector RAG!
        """
        if self.graph.number_of_nodes() == 0:
            return "No knowledge graph available."

        # Embed query
        query_embedding = self.embeddings.embed_query(query)

        # Find most similar nodes, using cosine similarity
        similarities = []
        for node, node_embedding in self.node_embeddings.items():
            sim = self._cosine_similarity(query_embedding, node_embedding)
            similarities.append((node, sim))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_nodes = [node for node, _ in similarities[:k]]

        if not top_nodes:
            return "No relevant information found in knowledge graph."

        # Extract subgraph around top nodes
        subgraph_nodes = set(top_nodes) #This means now, we extracted the most similar nodes

        #Now, we will also get their neighbours
        # Add neighbors (1-hop) to get context
        for node in top_nodes:
            neighbors = list(self.graph.neighbors(node))
            #self.graph.neighbors(node) returns all nodes directly connected to this node (1-hop away).
            subgraph_nodes.update(neighbors[:3])  # Add up to 3 neighbors per node

        # Build context from subgraph
        context = "=== RELEVANT KNOWLEDGE GRAPH SUBGRAPH ===\n\n"

        context += "\nRELATIONSHIPS:\n"
        # Add edges within subgraph
        edge_count = 0
        for source, target in self.graph.edges():
            if source in subgraph_nodes and target in subgraph_nodes:
                edge_data = self.graph.edges[source, target]
                relation = edge_data.get('relation', 'related_to') #We use related_to, as a placeholder if no relationship is found.
                source_text = self.graph.nodes[source].get('text', '')[:50]
                target_text = self.graph.nodes[target].get('text', '')[:50]
                context += f"  • {source_text}... --[{relation}]--> {target_text}...\n"
                edge_count += 1
                if edge_count >= 10:  # Limit to 10 relationships
                    break

        return context

# Define the state schema
class AgentState(TypedDict):
  """State schema for individual agent."""
  original_prompt: str
  harm_assessment: str #THIS WILL BE VERY USEFUL FOR LOGGING
  harm_level: str  # "safe", "mild", "moderate", "severe"
  transformed_prompt: str
  transformation_explanation: str #THIS WILL ALSO BE VERY USEFUL FOR LOGGING
  kg_context: str
  messages: Annotated[list, operator.add] #This allows us to accumulate log messages as the agent runs through different nodes

# ===============================================================================================
# INDIVIDUAL AGENT CLASS (with customizable assessment system and transformation system prompts)
# ===============================================================================================

class PromptSafetyAgent:
    """Individual agent with its own assessment and transformation nodes."""

    def __init__(
        self,
        agent_name: str,
        api_key: str,
        assessment_system_prompt: str,
        transformation_system_prompt: str,
        knowledge_docs_path: Optional[str] = None,
        model: str = "gpt-4o-mini"
    ):
        """
        Initialize a single safety agent.

        Args:
            agent_name: Name for this agent (for logging)
            api_key: OpenAI API key
            model: Model to use
            assessment_system_prompt: Custom system prompt for assessment
            transformation_system_prompt: Custom system prompt for transformation
        """
        self.agent_name = agent_name
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set as OPENAI_API_KEY env var")

        self.llm = ChatOpenAI(
            model=model,
            temperature=0.3,
            api_key=self.api_key
        )

        self.assessment_system_prompt = assessment_system_prompt
        self.transformation_system_prompt = transformation_system_prompt

        # Initialize knowledge graph
        self.knowledge_graph = TrueKnowledgeGraph(
            agent_name=agent_name,
            knowledge_docs_path=knowledge_docs_path,
            api_key=self.api_key
        )

        # Each agent has its own compiled graph!
        self.graph = self._build_graph()

    def _assess_harm(self, state: AgentState) -> AgentState:
        """Assess the harm level of the prompt."""

        # Retrieve subgraph (not just similar chunks)
        kg_context = self.knowledge_graph.retrieve_relevant_subgraph(
            state['original_prompt'],
            k=3
        )

        assessment_prompt = f"""Based on your areas of expertise, analyze the following prompt and:
        1. Identify any harmful, unethical, illegal, or inappropriate elements that violate your areas of expertise
        2. Classify the harm level as: "safe", "mild", "moderate", or "severe"
        3. Explain what makes it harmful (if applicable)

        You may take advantage of this knowledge graph's relationships, to identify issues.
        {kg_context}

        Prompt to analyze: "{state['original_prompt']}"

        Respond in the following format:
        HARM_LEVEL: [safe/mild/moderate/severe]
        ASSESSMENT: [detailed explanation]
        """

        print("🤖 " + self.agent_name + "\nAssessment Prompt: \n" + assessment_prompt) #MAYBE REMOVE LATER

        messages = [
            {"role": "system", "content": self.assessment_system_prompt},
            {"role": "user", "content": assessment_prompt}
        ]

        response = self.llm.invoke(messages)
        content = response.content

        # Parse response
        lines = content.split('\n')
        harm_level = "unknown"
        assessment = content

        for line in lines:
            if line.startswith("HARM_LEVEL:"):
                harm_level = line.split(":", 1)[1].strip().lower()
            elif line.startswith("ASSESSMENT:"):
                assessment = line.split(":", 1)[1].strip()

        return {
            **state,
            "harm_assessment": assessment,
            "harm_level": harm_level,
            "kg_context": kg_context,
            "messages": [f"[{self.agent_name}] Assessment: {harm_level}"]
        }

    def _transform_prompt(self, state: AgentState) -> AgentState:
        """Transform the prompt if harmful."""

        if state['harm_level'] == "safe":
            return {
                **state,
                "transformed_prompt": state['original_prompt'],
                "transformation_explanation": "No transformation needed - prompt is safe.",
                "messages": [f"[{self.agent_name}] No transformation needed"]
            }

        transformation_prompt = f"""Based on your areas of expertise, transform the following harmful prompt into a safe alternative that:
        1. Removes all harmful, unethical, illegal, or inappropriate elements, that violate your areas of expertise.
        2. Preserves the underlying legitimate intent (if any exists).
        3. Redirects toward positive, educational, or constructive purposes.
        4. The transformation must be no longer than the original.

        Original prompt: "{state['original_prompt']}"
        Harm assessment: {state['harm_assessment']}

        Provide:
        SAFE_PROMPT: [the transformed safe version]
        EXPLANATION: [how you transformed it]
        """

        messages = [
            {"role": "system", "content": self.transformation_system_prompt},
            {"role": "user", "content": transformation_prompt}
        ]

        response = self.llm.invoke(messages)
        content = response.content

        # Parse response
        lines = content.split('\n')
        safe_prompt = ""
        explanation = ""

        current_section = None
        for line in lines:
            if line.startswith("SAFE_PROMPT:"):
                current_section = "prompt"
                safe_prompt = line.split(":", 1)[1].strip()
            elif line.startswith("EXPLANATION:"):
                current_section = "explanation"
                explanation = line.split(":", 1)[1].strip()
            elif current_section == "prompt" and line.strip():
                safe_prompt += " " + line.strip()
            elif current_section == "explanation" and line.strip():
                explanation += " " + line.strip()

        return {
            **state,
            "transformed_prompt": safe_prompt or state['original_prompt'],
            "transformation_explanation": explanation or "Transformation applied.",
            "messages": [f"[{self.agent_name}] Transformed prompt"]
        }
        #We have or conditions in the result, incase the LLM fails to respond in the right format
        #If it fails to respond in the right format, this would cause the parsing to give empty strings
        #Which would then break the chain
        #So we use the original prompt, so that the chain can continue, incase the cleaning LLM makes a mistake

    def _build_graph(self) -> StateGraph:
        """Build this agent's internal graph."""

        workflow = StateGraph(AgentState)

        workflow.add_node("assess_harm", self._assess_harm)
        workflow.add_node("transform_prompt", self._transform_prompt)

        workflow.set_entry_point("assess_harm") #tells the graph where to start. When we run the workflow, it will begin at the "assess_harm" node.
        # Conditional routing based on harm assessment

        workflow.add_edge("assess_harm", "transform_prompt")  # Direct edge

        workflow.add_edge("transform_prompt", END)
        #After "transform_prompt" completes, go to END.
        #END is a special constant that terminates the workflow
        #No more nodes will run after this
        return workflow.compile()
        #compile() finalizes the workflow and makes it executable.
        #Returns a compiled graph that can process inputs.
        #After compilation, the graph can't be modified.

    def process(self, prompt: str) -> Dict:
        """
        Process a prompt through this agent's graph.

        Args:
            prompt: The prompt to process

        Returns:
            Dictionary with results that contains
            - agent_name: Name of the agent
            - original_prompt: The input prompt
            - harm_level: Classification of harm level
            - harm_assessment: Detailed assessment
            - transformed_prompt: Safe version of the prompt
            - transformation_explanation: How it was transformed
            - log messages
        """

        initial_state = {
            "original_prompt": prompt,
            "harm_assessment": "",
            "harm_level": "",
            "transformed_prompt": "",
            "transformation_explanation": "",
            "messages": []
        }

        result = self.graph.invoke(initial_state)

        return {
            "agent_name": self.agent_name,
            "original_prompt": result["original_prompt"],
            "kg_context": result["kg_context"],
            "harm_level": result["harm_level"],
            "harm_assessment": result["harm_assessment"],
            "transformed_prompt": result["transformed_prompt"],
            "transformation_explanation": result["transformation_explanation"],
            "messages": result["messages"]
        }

# ============================================================================
# MULTI-AGENT CHAIN STATE
# ============================================================================

class MultiAgentChainState(TypedDict):
    """State for the multi-agent chain system."""
    original_prompt: str

    # Results from each agent
    agent1_result: Dict
    agent2_result: Dict

    # The prompt passed between agents
    current_prompt: str

    # Final output
    final_safe_prompt: str

    # Aggregated logs
    all_messages: Annotated[List[str], operator.add]

# ============================================================================
# MULTI-AGENT CHAIN SYSTEM
# ============================================================================

class MultiAgentChainSystem:
    """
    System that chains 2 complete PromptSafetyAgent instances together.
    Each agent is a full LangGraph agent with assessment and transformation.
    """

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        Initialize the multi-agent chain system.

        Args:
            api_key: OpenAI API key
            model: Model to use for all agents
        """

        # Create 2 COMPLETE agents, each with their own LangGraph
        self.agent1 = PromptSafetyAgent(
            agent_name="Prompt Agent 1, Principles 1-3: Strengthening Human-Machine Ties, Safety, Algorithmic Bias",
            api_key=api_key,
            model=model,
            assessment_system_prompt= AGENT1_ASSESSMENT_PROMPT,
            transformation_system_prompt= AGENT1_TRANSFORMATION_PROMPT,
            knowledge_docs_path= "Agent_1"
        )

        self.agent2 = PromptSafetyAgent(
            agent_name="Prompt Agent 2, Principles 4-6: Data Privacy, Transparency, Human Oversight",
            api_key=api_key,
            model=model,
            assessment_system_prompt= AGENT2_ASSESSMENT_PROMPT,
            transformation_system_prompt= AGENT2_TRANSFORMATION_PROMPT,
            knowledge_docs_path= "Agent_2"
        )

        # Build the outer chain graph that connects the 2 agents
        self.chain_graph = self._build_chain_graph()

    def _run_agent1(self, state: MultiAgentChainState) -> MultiAgentChainState:
        """Run Agent 1 on the original prompt."""

        # Agent 1 receives the ORIGINAL prompt
        input_prompt = state['original_prompt']

        # Process through Agent 1's FULL graph (assessment + transformation)
        result = self.agent1.process(input_prompt)

        return {
            **state,
            "agent1_result": result,
            "current_prompt": result['transformed_prompt'],  # Pass to next agent
            "all_messages": [f"🤖 Agent 1 processed: {result['harm_level']}"]
        }

    def _run_agent2(self, state: MultiAgentChainState) -> MultiAgentChainState:
        """Run Agent 2 on Agent 1's output."""

        # Agent 2 receives the CLEANED prompt from Agent 1
        input_prompt = state['current_prompt']

        # Process through Agent 2's FULL graph
        result = self.agent2.process(input_prompt)

        return {
            **state,
            "agent2_result": result,
            "current_prompt": result['transformed_prompt'],
            "final_safe_prompt": result['transformed_prompt'],  # Final output!
            "all_messages": [f"🤖 Agent 2 processed: {result['harm_level']}"]
        }

    def _build_chain_graph(self) -> StateGraph:
        """Build the outer graph that chains the 2 agents together."""

        workflow = StateGraph(MultiAgentChainState)

        # Add nodes for each agent
        workflow.add_node("agent1", self._run_agent1)
        workflow.add_node("agent2", self._run_agent2)

        # Chain them sequentially
        workflow.set_entry_point("agent1")
        workflow.add_edge("agent1", "agent2")
        workflow.add_edge("agent2", END)

        return workflow.compile()

    def visualize_flow(self, result: Dict):
        print("\n" + "="*100)
        print("TRUE GRAPHRAG UAE CHARTER MULTI-AGENT SYSTEM")
        print("="*100)

        # NEW: Show GRAPH statistics (not vector counts)
        print("\n📊 KNOWLEDGE GRAPH STATISTICS:")
        for i, agent in enumerate([self.agent1, self.agent2], 1):
            kg = agent.knowledge_graph
            if kg.graph.number_of_nodes() > 0:
                nodes = kg.graph.number_of_nodes()
                edges = kg.graph.number_of_edges()
                print(f"   Prompt Agent {i}: ✓ GRAPH ({nodes} nodes, {edges} edges)")
            else:
                print(f"   Prompt Agent {i}: ✗ NO GRAPH")

        print(f"\n📝 ORIGINAL: {result['original_prompt']}\n")

        for i, agent_result in enumerate(result['agents'], 1):
            print(f"{'─'*100}")
            print(f"🤖 {agent_result['agent_name']}")
            print(f"{'─'*100}")
            print(f"   In:  {agent_result['original_prompt']}")
            print(f"   Level: {agent_result['harm_level'].upper()}")

            # Show graph usage
            graph_used = any("graph" in msg.lower() for msg in agent_result.get('messages', []))
            if graph_used:
                print(f"   📊 [Knowledge Graph Queried - Subgraph Retrieved]")

            print(f"   Found: {agent_result['harm_assessment']}")
            print(f"   Out: {agent_result['transformed_prompt']}")
            print(f"   Why: {agent_result['transformation_explanation']}")
            if i < len(result['agents']):
                print(f"   ↓")

        print(f"\n{'='*100}")
        print(f"✅ FINAL: {result['final_safe_prompt']}")
        print(f"{'='*100}\n")

    def process_prompt(self, prompt: str) -> Dict:
        """
        Process a prompt through all 4 chained agents.

        Args:
            prompt: The original prompt to process

        Returns:
            Dictionary with results from all agents
        """

        initial_state = {
            "original_prompt": prompt,
            "agent1_result": {},
            "agent2_result": {},
            "current_prompt": prompt,
            "final_safe_prompt": "",
            "all_messages": []
        }

        # Run the chain graph
        result = self.chain_graph.invoke(initial_state)

        #self.visualize_flow( {
        #    "original_prompt": result["original_prompt"],
        #    "final_safe_prompt": result["final_safe_prompt"],
        #    "agents": [
        #        result["agent1_result"],
        #        result["agent2_result"],
        #        result["agent3_result"],
        #        result["agent4_result"]
        #    ],
        #    "processing_log": result["all_messages"]
        #})

        #return (result["final_safe_prompt"].strip('"'))
        return result
