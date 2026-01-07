## LlamaStack Server

### Prerequisites
- OPENAI_API_KEY set in `.env` at repo root

### Running the Server
```bash
make llama-server
```

Server runs on http://localhost:8321

### Testing the Server
```bash
curl http://localhost:8321/v1/models
```

### Running Patterns
```bash
uv run llamastack-prompt-chaining
VERBOSE=true uv run llamastack-prompt-chaining
```

## OpenAI Responses API with LlamaStack

### Key Finding: Responses API requires the `agents` API

The OpenAI Responses API in LlamaStack is **part of the agents provider**, not the inference provider. This means you cannot use `client.responses.create()` with just the inference API enabled.

### Dependency Chain

The agents API has a dependency chain that must be satisfied:

```
agents → requires → vector_io, tool_runtime
tool_runtime → requires → files
```

### Required APIs and Providers

| API | Provider | Purpose |
|-----|----------|---------|
| `inference` | `remote::openai` | LLM inference (chat completions, embeddings) |
| `agents` | `inline::meta-reference` | **Exposes the Responses API** (`/v1/responses`) |
| `vector_io` | `inline::faiss` | Vector storage (required by agents) |
| `tool_runtime` | `inline::rag-runtime` | Tool execution (required by agents) |
| `files` | `inline::localfs` | File storage (required by tool_runtime) |

### Configuration Notes (v0.4.0+)

Breaking changes in LlamaStack v0.4.0:

1. **FaissVectorIOConfig**: Changed from `kvstore` to `persistence` field referencing a storage backend
2. **Agents provider**: Changed from `persistence_store` to nested `persistence.agent_state` and `persistence.responses`
3. **URL structure**: The `/openai/v1` path was removed; use `/v1` directly

### Example: Using Responses API

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8321/v1", api_key="none")

response = client.responses.create(
    model="openai/gpt-4o-mini",
    input="Extract technical specs from: The laptop has 16GB RAM and 1TB SSD",
)
print(response.output_text)
```

### ODH Dashboard Reference

The [ODH Dashboard BFF](https://github.com/opendatahub-io/odh-dashboard/tree/main/packages/gen-ai/bff) uses the Responses API (not Chat Completions) for their LlamaStack integration:
- `client.Responses.New()` for synchronous responses
- `client.Responses.NewStreaming()` for streaming responses

## LlamaStack as an Infrastructure Layer

### Orchestration: Manual vs Framework

LlamaStack provides a **standardized API layer** (OpenAI-compatible), not workflow orchestration. For patterns like prompt chaining, you have two options:

| Approach | Pros | Cons |
|----------|------|------|
| **Pure LlamaStack** | Portable, no framework lock-in, lighter weight | Manual orchestration |
| **LangChain + LlamaStack backend** | Rich abstractions, familiar patterns | Extra dependency |

**Hybrid approach** - Use LlamaStack as backend with LangChain for orchestration:

```python
from langchain_openai import ChatOpenAI

# LlamaStack as the backend
llm = ChatOpenAI(
    base_url="http://localhost:8321/v1",
    api_key="none",
    model="openai/gpt-4o-mini"
)

# LangChain's LCEL for orchestration
chain = prompt1 | llm | parser | prompt2 | llm
```

### Benefits of LlamaStack as Infrastructure

**1. Model Freedom**
```yaml
# Today: OpenAI
providers:
  inference:
    - provider_type: remote::openai

# Tomorrow: Local vLLM (no app code changes)
providers:
  inference:
    - provider_type: remote::vllm
      config:
        url: http://my-vllm-server:8000/v1
```

**2. Data Sovereignty**
- Prompts/data never leave your infrastructure
- Critical for regulated industries (healthcare, finance, government)

**3. Unified API across heterogeneous backends**
- OpenAI, Ollama, vLLM, TGI, local Llama models → all become the same API
- Application code doesn't know or care what's behind it

**4. Infrastructure-level controls**
- Safety shields (content moderation) at the gateway
- Telemetry/observability
- Auth/access control
- Model routing (e.g., simple queries → cheap model, complex → expensive)

**5. Avoid double lock-in**
- Without LlamaStack: locked into both orchestration framework AND provider's API
- With LlamaStack: only orchestration patterns (backend is swappable)

**6. Drop-in replacement**

From [Red Hat Developer](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack):
> "Because Llama Stack implements the OpenAI-compatible Responses API, you can use it as a **drop-in replacement** for a proprietary, hosted endpoint."

- Compatible with LangChain, OpenAI Python client, and other OpenAI-compatible tools
- Minimal code changes to switch from proprietary services
- Seamless integration with existing agent and chain logic

### Architecture Mental Model

```
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│         (Your code, LangChain, ADK, etc.)               │
└─────────────────────────┬───────────────────────────────┘
                          │ OpenAI-compatible API
┌─────────────────────────▼───────────────────────────────┐
│                 LlamaStack (Infrastructure)              │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │ Inference│ │  Agents  │ │ Vector IO│ │  Safety  │  │
│   └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
└────────┼────────────┼────────────┼────────────┼────────┘
         │            │            │            │
┌────────▼────────────▼────────────▼────────────▼────────┐
│                    Model Providers                       │
│   OpenAI  │  vLLM  │  Ollama  │  TGI  │  Local Llama   │
└─────────────────────────────────────────────────────────┘
```

LlamaStack is the **LLM infrastructure layer**; LangChain/ADK are the **orchestration layer**. They solve different problems and can complement each other.

> **Note:** For more complex agentic patterns (routing, parallelization, orchestrator-workers, evaluator-optimizer), consider using LangChain/LangGraph on top of LlamaStack. The manual orchestration approach works well for simple patterns like prompt chaining, but the complexity grows quickly. Using LlamaStack as the backend preserves model freedom while leveraging LangChain's battle-tested orchestration abstractions.

### Confirmed by Official Sources

This infrastructure layer positioning is confirmed by LlamaStack's official documentation:

**From [GitHub](https://github.com/llamastack/llama-stack):**
> "Composable building blocks to build LLM Apps"

**From [Official Docs](https://llamastack.github.io/docs):**
> "Unified API layer for Inference, RAG, Agents, Tools, Safety, Evals"
>
> "Plugin architecture to support the rich ecosystem of different API implementations"
>
> "Developers can choose their preferred infrastructure without changing APIs"

**From the README:**
> "LlamaStack defines and standardizes the core building blocks needed to bring generative AI applications to market"
>
> "Start iterating on local, mobile or desktop and seamlessly transition to on-prem or public cloud deployments"

The official docs explicitly use **"building blocks"** and **"unified API layer"** language, not "orchestration" or "workflow" language. This confirms LlamaStack's role as infrastructure, not an orchestration framework.

| Framework | Self-Description | Role |
|-----------|------------------|------|
| **LlamaStack** | "Composable building blocks", "Unified API layer" | Infrastructure |
| **LangChain** | "Orchestration framework", "Chains", "Agents" | Orchestration |

## Sources and References

### Responses API
- [OpenAI - Why We Built the Responses API](https://developers.openai.com/blog/responses-api/) - The design philosophy behind the Responses API

### Official LlamaStack Documentation
- [LlamaStack GitHub Repository](https://github.com/llamastack/llama-stack)
- [LlamaStack Official Docs](https://llamastack.github.io/docs)
- [LlamaStack OpenAI Compatibility](https://llamastack.github.io/docs/providers/openai)

### Red Hat Developer Articles
- [Deep dive into Responses API with Llama Stack](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack)
- [Migrating to Responses API](https://developers.redhat.com/articles/2025/12/09/your-ai-agents-evolved-modernize-llama-stack-agents-migrating-responses-api)

### OpenDataHub
- [Working with LlamaStack](https://opendatahub.io/docs/working-with-llama-stack/)
- [ODH Dashboard gen-ai BFF source](https://github.com/opendatahub-io/odh-dashboard/tree/main/packages/gen-ai/bff)

### Additional Resources
- [LangChain Integration Guide for Llama](https://www.llama.com/docs/integration-guides/langchain/)
- [Getting started with Llama Stack - Niklas Heidloff](https://heidloff.net/article/llama-stack/)
