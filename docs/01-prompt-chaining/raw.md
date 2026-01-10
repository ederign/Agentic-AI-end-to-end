# Prompt Chaining: Raw Approach (LlamaStack Responses API)

## Understanding the Responses API

Before diving into LlamaStack's implementation, it's important to understand why the Responses API matters.

### Why OpenAI Built the Responses API

From [OpenAI's blog](https://developers.openai.com/blog/responses-api/):

> "Something as approachable as Chat Completions, as powerful as Assistants, but also purpose built for multimodal and reasoning models."

**Problems it solves:**

| Chat Completions API | Responses API |
|---------------------|---------------|
| Drops context between calls | Preserves reasoning state across interactions |
| Text-only focus | Native multimodal support (text, images, audio, tools) |
| Simple request/response | Sophisticated agentic workflows |
| Manual state management | Built-in hosted tools (file search, code interpreter) |

**Key innovations:**
- **Reasoning loop** - Maintains the model's thought process across interactions
- **Multiple output items** - Emits tool calls, intermediate steps, not just text
- **Better performance** - 40-80% improved cache utilization
- **Stateful by design** - Purpose-built for agentic applications

### Why This Matters for LlamaStack

LlamaStack implements the OpenAI-compatible Responses API, which means:
- You get the same powerful API for agentic workflows
- But with model freedom, data sovereignty, and no vendor lock-in
- Your code works with both OpenAI and LlamaStack

---

## Approach

LlamaStack provides **building blocks** (OpenAI-compatible API), not orchestration. Prompt chaining is implemented manually by calling the API sequentially.

## Why Responses API? (Legacy Agents API Deprecation)

LlamaStack is migrating from the legacy Agents API to the OpenAI-compatible Responses API. Key reasons:

| Legacy Agents API | Responses API |
|-------------------|---------------|
| Explicit lifecycle management | Automated orchestration |
| Manual tool discovery | Automatic tool discovery |
| Custom code for multi-step reasoning | Built-in multi-step reasoning |
| Framework-specific patterns | OpenAI-compatible (portable) |

**Benefits of the migration:**

1. **Simplified orchestration** - No need to "explicitly manage every aspect of agent lifecycle"
2. **Advanced reasoning** - Built-in support for "multi-step reasoning and automatic tool chaining"
3. **Industry alignment** - Matches the trend toward server-side agentic operations
4. **Reduced complexity** - What was "cumbersome to implement" becomes "a natural extension of the standard flow"

> The migration is "an opportunity to simplify your code, improve agent capabilities, and position your system for future innovations."
> — [Red Hat Developer](https://developers.redhat.com/articles/2025/12/09/your-ai-agents-evolved-modernize-llama-stack-agents-migrating-responses-api)

## Key Finding: Responses API Requires Agents Provider

The OpenAI Responses API (`client.responses.create()`) is **part of the agents provider**, not inference. This requires enabling multiple APIs:

```
agents → requires → vector_io, tool_runtime
tool_runtime → requires → files
```

## Implementation

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

## Configuration Requirements

LlamaStack v0.4.0+ requires this configuration for Responses API:

```yaml
apis:
  - inference
  - agents        # Required for Responses API
  - files         # Required by tool_runtime
  - tool_runtime  # Required by agents
  - vector_io     # Required by agents

providers:
  inference:
    - provider_type: remote::openai
  agents:
    - provider_type: inline::meta-reference
  files:
    - provider_type: inline::localfs
  vector_io:
    - provider_type: inline::faiss
  tool_runtime:
    - provider_type: inline::rag-runtime
```

## Strengths

- **No framework lock-in** - Standard OpenAI client
- **Model portability** - Swap providers via config, not code
- **Data sovereignty** - Run entirely in your infrastructure
- **Simple code** - Just API calls, no abstractions to learn
- **Predictable** - Explicit control over every step

## Weaknesses

- **Manual orchestration** - No built-in chaining abstractions
- **More boilerplate** - Must handle data passing explicitly
- **Complex setup** - Many dependencies for Responses API
- **Scaling complexity** - Complex patterns require more code

## Key Insight

LlamaStack is an **infrastructure layer**, not an orchestration framework. For simple patterns like prompt chaining, manual orchestration is fine. For complex patterns, consider using **LangChain on top of LlamaStack**.

### Confirmed by Official Sources

From [Red Hat Developer - Responses API Deep Dive](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack):

> "Because Llama Stack implements the OpenAI-compatible Responses API, you can use it as a **drop-in replacement** for a proprietary, hosted endpoint."

**Three core benefits:**

| Benefit | Description |
|---------|-------------|
| **Model Freedom** | Choose from various inference providers (OpenAI, vLLM, Ollama, local models) |
| **Data Sovereignty** | Keep sensitive data within your secure infrastructure |
| **No Vendor Lock-in** | Open, extensible stack - switch providers without code changes |

**Drop-in replacement features:**
- Compatible with LangChain, OpenAI Python client, and other OpenAI-compatible tools
- Minimal code changes to switch from proprietary services
- Seamless integration with existing agent and chain logic

### Hybrid Approach: LangChain + LlamaStack

```python
from langchain_openai import ChatOpenAI

# LlamaStack as infrastructure
llm = ChatOpenAI(
    base_url="http://localhost:8321/v1",
    api_key="none",
    model="openai/gpt-4o-mini"
)

# LangChain for orchestration
chain = prompt1 | llm | parser | prompt2 | llm
```

## Code Location

`packages/patterns/src/patterns/prompt_chaining/raw.py`

## Running

```bash
# Start LlamaStack server first
make llama-server

# Run the pattern
make prompt-chaining-raw
# or
uv run --package patterns prompt-chaining --approach raw
```

## References

### Responses API
- [OpenAI - Why We Built the Responses API](https://developers.openai.com/blog/responses-api/) - The design philosophy behind the Responses API

### LlamaStack
- [LlamaStack GitHub](https://github.com/llamastack/llama-stack)
- [Red Hat Developer - Responses API Deep Dive](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack)
- [Red Hat Developer - Migrating to Responses API](https://developers.redhat.com/articles/2025/12/09/your-ai-agents-evolved-modernize-llama-stack-agents-migrating-responses-api) - Why LlamaStack is deprecating the legacy Agents API

### Real-World Usage
- [ODH Dashboard BFF](https://github.com/opendatahub-io/odh-dashboard/tree/main/packages/gen-ai/bff) - Production Responses API usage in Go
