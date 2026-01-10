# Pattern 1: Prompt Chaining

> **Repository with samples:** [github.com/ederign/Agentic-AI-end-to-end](https://github.com/ederign/Agentic-AI-end-to-end)
>
> **Note:** These findings emerged from collaborative exploration with Claude (Anthropic), including hands-on implementation and documentation research.

## What is Prompt Chaining?

Prompt chaining is the simplest agentic pattern: a sequence of LLM calls where the output of one step becomes the input for the next. It's the foundation for more complex patterns.

```
Input → [Prompt 1] → Output₁ → [Prompt 2] → Output₂ → ... → Final Result
```

## Why Prompt Chaining?

While a single, detailed prompt can work for simpler tasks, complex workflows benefit from breaking work into sequential steps. This **divide-and-conquer** approach offers several advantages:

- **Simpler prompts** - Each step has a focused, well-defined task
- **Easier debugging** - You can inspect intermediate outputs between steps
- **Better accuracy** - Smaller, focused prompts tend to produce more reliable results
- **Structured outputs** - Each step can enforce specific output formats (JSON, bullet points, etc.)

Prompt chaining is particularly effective when tasks have clear sequential dependencies—where Step 2 genuinely needs the output of Step 1 to proceed.

## Use Cases

- **Data extraction and transformation** - Extract info → Clean → Format
- **Multi-stage reasoning** - Analyze → Critique → Refine
- **Content generation pipelines** - Outline → Draft → Edit → Polish
- **Validation workflows** - Generate → Validate → Fix if needed

## Our Example: Specs Extraction

This example is adapted from the book's prompt chaining chapter. All three implementations solve the same problem:

```
Input: "The laptop has a 3.5 GHz octa-core processor, 16GB RAM, and 1TB NVMe SSD"
     ↓
[Step 1: Extract] → Bullet points of specs
     ↓
[Step 2: Transform] → Structured JSON
     ↓
Output: {"cpu": "3.5 GHz octa-core", "memory": "16GB", "storage": "1TB NVMe SSD"}
```

---

## Approach 1: OpenAI APIs (LlamaStack)

LlamaStack provides **building blocks** (OpenAI-compatible API), not orchestration. Prompt chaining is implemented manually by calling the API sequentially.

### Why the Responses API?

From [OpenAI's blog](https://developers.openai.com/blog/responses-api/):

> "Something as approachable as Chat Completions, as powerful as Assistants, but also purpose built for multimodal and reasoning models."

LlamaStack implements the OpenAI-compatible Responses API, which means:
- You get the same powerful API for agentic workflows
- But with model freedom, data sovereignty, and no vendor lock-in

### Implementation

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8321/v1", api_key="none")
MODEL = "openai/gpt-4o-mini"

# Step 1: Extract specifications
extraction_response = client.responses.create(
    model=MODEL,
    input=(
        "Extract the technical specifications from the following text:\n\n"
        f"{text_input}\n\n"
        "Return only the extracted specs as concise bullet points."
    ),
)
specifications = extraction_response.output_text

# Step 2: Transform to JSON (using output from step 1)
transform_response = client.responses.create(
    model=MODEL,
    input=(
        "Transform the following specifications into a JSON object with "
        "'cpu', 'memory', and 'storage' as keys:\n\n"
        f"{specifications}\n\n"
        "Return only valid JSON, no markdown or extra text."
    ),
)
json_text = transform_response.output_text
```

### Strengths

- **No framework lock-in** - Standard OpenAI client
- **Model portability** - Swap providers via config, not code
- **Data sovereignty** - Run entirely in your infrastructure
- **Simple code** - Just API calls, no abstractions to learn

### Weaknesses

- **Manual orchestration** - No built-in chaining abstractions
- **More boilerplate** - Must handle data passing explicitly
- **Scaling complexity** - Complex patterns require more code

### Running

```bash
make llama-server  # Start LlamaStack first
make prompt-chaining-raw
```

---

## Approach 2: LangChain + LlamaStack

LangChain uses **LCEL (LangChain Expression Language)** to compose chains declaratively using the `|` operator, with LlamaStack as the infrastructure backend.

### Key Concepts

- **ChatPromptTemplate** - Defines prompt templates with variables
- **StrOutputParser** - Converts LLM output to string
- **LCEL Pipe (`|`)** - Chains components together
- **Dictionary mapping** - Passes outputs to named variables

### Implementation

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:8321/v1",  # LlamaStack
    api_key="none",
    model="openai/gpt-4o-mini",
    temperature=0,
)

# Step 1: Extract specifications
prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)

# Step 2: Transform to JSON
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with "
    "'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

# Build chain using LCEL
extraction_chain = prompt_extract | llm | StrOutputParser()

full_chain = (
    {"specifications": extraction_chain}  # Output becomes 'specifications' variable
    | prompt_transform
    | llm
    | StrOutputParser()
)

# Execute
result = full_chain.invoke({"text_input": "The laptop has 16GB RAM..."})
```

### Strengths

- **Declarative syntax** - Easy to read and understand flow
- **Automatic data passing** - LCEL handles variable mapping
- **Composable** - Chains can be nested and combined
- **Streaming support** - Built-in streaming capabilities

### Weaknesses

- **Framework lock-in** - Code tied to LangChain abstractions
- **Magic behavior** - Data flow can be non-obvious for complex chains
- **Learning curve** - Need to understand LCEL semantics

### Running

```bash
make llama-server  # Start LlamaStack first
make prompt-chaining-langchain
```

---

## Approach 3: ADK (Google Agent Development Kit)

ADK uses **SequentialAgent** to chain multiple **LlmAgent** instances. State is passed between agents via a shared state dictionary. Uses LiteLLM as infrastructure.

### Key Concepts

- **LlmAgent** - Individual agent with model, instruction, and output configuration
- **SequentialAgent** - Runs sub-agents in order
- **State dictionary** - Shared context between agents
- **output_key** - Where agent stores its result in state
- **output_schema** - Pydantic model for structured output

### Why Dynamic Instructions? (Lazy Evaluation)

ADK only interpolates `{variables}` from the **initial state**. Values added by previous agents aren't automatically available in template strings. The solution is to pass a function that ADK calls **when the agent runs**:

```python
def build_transform_instruction(ctx: ReadonlyContext) -> str:
    specs = ctx.state.get("specifications", "")  # Read at run time
    return f"Transform to JSON:\n\n{specs}"
```

### Implementation

```python
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import InMemoryRunner
from pydantic import BaseModel, Field

MODEL = "openai/gpt-4o-mini"

class SpecsJson(BaseModel):
    cpu: str = Field(description="CPU details")
    memory: str = Field(description="RAM size")
    storage: str = Field(description="Storage details")

# Step 1: Extract agent
extract_agent = LlmAgent(
    name="extract_specs_agent",
    model=MODEL,
    instruction=(
        "Extract the technical specifications from the following text:\n\n"
        "{user_text}\n\n"
        "Return only the extracted specs as concise bullet points."
    ),
    output_key="specifications",
)

# Step 2: Transform agent
def build_transform_instruction(ctx):
    specs = ctx.state.get("specifications", "")
    return f"Transform to JSON with cpu, memory, storage keys:\n\n{specs}"

transform_agent = LlmAgent(
    name="transform_specs_agent",
    model=MODEL,
    instruction=build_transform_instruction,
    output_schema=SpecsJson,
    output_key="result",
)

# Build pipeline
pipeline = SequentialAgent(
    name="specs_pipeline",
    sub_agents=[extract_agent, transform_agent],
)
```

### Strengths

- **Structured agents** - Clear agent definitions with explicit configuration
- **Type safety** - output_schema with Pydantic validation
- **State management** - Built-in state passing between agents
- **Reusable agents** - Agents can be composed into different pipelines

### Weaknesses

- **More boilerplate** - Async setup, sessions, runners required
- **Complex execution** - Need to manage sessions and async flow
- **Learning curve** - More concepts to understand (agents, runners, sessions)

### Running

```bash
make prompt-chaining-adk  # No LlamaStack needed, uses LiteLLM
```

---

## Comparison

### Summary Table

| Aspect | OpenAI APIs | LangChain | ADK |
|--------|-------------|-----------|-----|
| **Infrastructure** | LlamaStack | LlamaStack | LiteLLM |
| **Orchestration** | Manual | LCEL chains | SequentialAgent |
| **Data passing** | Manual | Automatic via dict | State dictionary | 
| **Async required** | No | No | Yes |
| **Framework lock-in** | None | High | High |

### Code Comparison

```python
# OpenAI APIs - Explicit API calls
response1 = client.responses.create(model=MODEL, input=prompt1)
response2 = client.responses.create(model=MODEL, input=f"{prompt2}\n{response1.output_text}")

# LangChain - Declarative pipeline
chain = {"specs": prompt1 | llm | parser} | prompt2 | llm | parser
result = chain.invoke({"text_input": input})

# ADK - Structured agents
pipeline = SequentialAgent(sub_agents=[extract_agent, transform_agent])
async for event in runner.run_async(...): ...
```

### Recommendation Matrix

| Scenario | Recommended Approach |
|----------|---------------------|
| Quick prototype | LangChain |
| Production with model flexibility | LangChain + LlamaStack |
| Data sovereignty requirements | OpenAI APIs (LlamaStack) |
| Multi-agent systems | ADK |
| Minimal dependencies | OpenAI APIs (LlamaStack) |

---

## Running All Approaches

```bash
# Start LlamaStack (required for OpenAI APIs and LangChain)
make llama-server

# Run individual approaches
make prompt-chaining-raw       # OpenAI APIs
make prompt-chaining-langchain # LangChain
make prompt-chaining-adk       # ADK

# Compare all three
make prompt-chaining-all
```

## Code Location

- `packages/patterns/src/patterns/prompt_chaining/raw.py` - OpenAI APIs
- `packages/patterns/src/patterns/prompt_chaining/langchain.py` - LangChain
- `packages/patterns/src/patterns/prompt_chaining/adk.py` - ADK

## References

- [Agentic Design Patterns](https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018) by Antonio Gullí - The book that serves as the basis for this project
- [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [OpenAI - Why We Built the Responses API](https://developers.openai.com/blog/responses-api/)
- [LlamaStack GitHub](https://github.com/llamastack/llama-stack)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Red Hat - Responses API Deep Dive](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack)
