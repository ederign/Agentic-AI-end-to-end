# Frameworks Overview

## The Three Frameworks

### LangChain / LangGraph

**Role:** Orchestration Framework

LangChain is a comprehensive orchestration framework for building LLM applications. It provides high-level abstractions for common patterns.

**Key Characteristics:**
- Rich ecosystem of chains, agents, and tools
- LCEL (LangChain Expression Language) for composable pipelines
- LangGraph for stateful, graph-based agent workflows
- Extensive integrations with vector stores, APIs, and tools

**Self-Description:**
> "A powerful open-source orchestration framework designed for building LLM applications"

**Best For:**
- Rapid prototyping
- Complex multi-step workflows
- Teams wanting battle-tested abstractions

---

### LlamaStack

**Role:** Infrastructure Layer

LlamaStack provides a unified, OpenAI-compatible API layer that abstracts model providers. It's not an orchestration framework—it's the infrastructure that orchestration frameworks can run on top of.

**Key Characteristics:**
- OpenAI-compatible Responses API
- Plugin architecture for multiple providers (OpenAI, vLLM, Ollama, etc.)
- Built-in safety, telemetry, and evaluation capabilities
- Model freedom without code changes

**Self-Description (from official docs):**
> "Composable building blocks to build LLM Apps"
>
> "Unified API layer for Inference, RAG, Agents, Tools, Safety, Evals"
>
> "Developers can choose their preferred infrastructure without changing APIs"
>
> "Because Llama Stack implements the OpenAI-compatible Responses API, you can use it as a **drop-in replacement** for a proprietary, hosted endpoint."
> — [Red Hat Developer](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack)

**Three Core Benefits:**
- **Model Freedom** - Choose from various inference providers
- **Data Sovereignty** - Keep sensitive data within your infrastructure
- **No Vendor Lock-in** - Open, extensible stack

**Best For:**
- Model portability (switch providers without code changes)
- Data sovereignty (run models in your infrastructure)
- Enterprise deployments with compliance requirements

---

### ADK (Agent Development Kit)

**Role:** Orchestration Framework

Google's Agent Development Kit provides a structured approach to building AI agents with emphasis on tool usage and multi-agent coordination.

**Key Characteristics:**
- Structured agent definitions
- Built-in tool integration
- Support for multi-agent systems
- Google Cloud integration

**Best For:**
- Google Cloud ecosystem users
- Structured agent development
- Teams preferring explicit agent definitions

---

## Architecture Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Code                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              Orchestration Layer (choose one)                │
│                                                              │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│   │  LangChain   │  │     ADK      │  │  Your Code   │     │
│   │  LangGraph   │  │              │  │  (manual)    │     │
│   └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────┬───────────────────────────────────┘
                          │ OpenAI-compatible API
┌─────────────────────────▼───────────────────────────────────┐
│              Infrastructure Layer (optional)                 │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                    LlamaStack                        │   │
│   │  (Unified API, Safety, Telemetry, Model Routing)    │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Model Providers                           │
│                                                              │
│   OpenAI  │  vLLM  │  Ollama  │  TGI  │  Anthropic  │  ... │
└─────────────────────────────────────────────────────────────┘
```

## Decision Matrix

| Consideration | LangChain | LlamaStack | ADK |
|---------------|-----------|------------|-----|
| **Primary Role** | Orchestration | Infrastructure | Orchestration |
| **Abstraction Level** | High | Low | Medium |
| **Model Lock-in** | Via integrations | None (unified API) | Google-focused |
| **Learning Curve** | Medium | Low | Medium |
| **Built-in Patterns** | Many | Few (building blocks) | Some |
| **Self-hosting** | N/A | Core feature | Limited |
| **Enterprise Features** | Via LangSmith | Built-in | Via Google Cloud |

## Hybrid Approach: LangChain + LlamaStack

For maximum flexibility, consider using LangChain for orchestration with LlamaStack as the backend:

```python
from langchain_openai import ChatOpenAI

# LlamaStack provides the infrastructure
llm = ChatOpenAI(
    base_url="http://localhost:8321/v1",  # LlamaStack server
    api_key="none",
    model="openai/gpt-4o-mini"
)

# LangChain provides the orchestration
chain = prompt | llm | parser
```

**Benefits:**
- Model freedom (swap providers via LlamaStack config)
- Rich abstractions (LangChain's chains, agents, tools)
- Data sovereignty (LlamaStack can run locally)
- Best of both worlds

---

## References

### Official Documentation
- [LlamaStack GitHub](https://github.com/llamastack/llama-stack)
- [LlamaStack Docs](https://llamastack.github.io/docs)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)

### Responses API
- [OpenAI - Why We Built the Responses API](https://developers.openai.com/blog/responses-api/) - The design philosophy behind the Responses API

### Articles and Guides
- [Red Hat Developer - Deep dive into Responses API with Llama Stack](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack)
- [Red Hat Developer - Migrating to Responses API](https://developers.redhat.com/articles/2025/12/09/your-ai-agents-evolved-modernize-llama-stack-agents-migrating-responses-api)
- [OpenDataHub - Working with LlamaStack](https://opendatahub.io/docs/working-with-llama-stack/)
- [LangChain Integration Guide for Llama](https://www.llama.com/docs/integration-guides/langchain/)
- [Getting started with Llama Stack - Niklas Heidloff](https://heidloff.net/article/llama-stack/)

### Code References
- [ODH Dashboard gen-ai BFF](https://github.com/opendatahub-io/odh-dashboard/tree/main/packages/gen-ai/bff) - Real-world LlamaStack usage with Responses API
