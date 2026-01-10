# Bibliography & Resources

> **Note:** This catalog was curated through collaborative exploration with Claude (Anthropic). Each link includes a summary based on content review.

## Quick Navigation

- [Core Concepts](#core-concepts)
- [Framework Documentation](#framework-documentation)
- [Pattern-Specific Resources](#pattern-specific-resources)
- [Real-World Examples](#real-world-examples)

---

## Core Concepts

### Responses API

| Resource | Summary |
|----------|---------|
| [OpenAI - Why We Built the Responses API](https://developers.openai.com/blog/responses-api/) | OpenAI's design philosophy for the Responses API. Explains why they built it: "as approachable as Chat Completions, as powerful as Assistants, purpose-built for multimodal and reasoning models." Key innovations include reasoning loops, stateful interactions, and 40-80% improved cache utilization. |

### Agentic AI Patterns

| Resource | Summary |
|----------|---------|
| [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | Anthropic's guide to agentic design patterns including prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer. Foundation for understanding agentic architectures. |

---

## Framework Documentation

### LlamaStack

| Resource | Summary |
|----------|---------|
| [LlamaStack GitHub](https://github.com/llamastack/llama-stack) | Official repository. Self-described as "Composable building blocks to build LLM Apps." Provides unified API layer for inference, RAG, agents, tools, safety, and evals with plugin architecture for multiple providers. |
| [LlamaStack Official Docs](https://llamastack.github.io/docs) | Main documentation. Covers distributions, providers, APIs, and deployment options. Key message: "Developers can choose their preferred infrastructure without changing APIs." |
| [LlamaStack OpenAI Compatibility](https://llamastack.github.io/docs/providers/openai) | Details on OpenAI-compatible API endpoints. Shows how to use OpenAI client with LlamaStack: `base_url="http://localhost:8321/v1"`. |

### LangChain / LangGraph

| Resource | Summary |
|----------|---------|
| [LangChain Documentation](https://python.langchain.com/docs/) | Open source framework for building AI agents. Features LCEL (LangChain Expression Language) for composable pipelines, standard model interface, and integration with LangSmith for debugging. "Under 10 lines of code to connect to OpenAI, Anthropic, Google, and more." |
| [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) | Low-level orchestration framework for stateful, multi-actor LLM applications. Models workflows as directed graphs with nodes (agents/components) and edges (information flow). Key features: state management, durable execution, human-in-the-loop, cyclical workflows. |
| [LangGraph GitHub](https://github.com/langchain-ai/langgraph) | "Build resilient language agents as graphs." Trusted by Klarna, Replit, Elastic. Supports both short-term working memory and long-term persistent memory across sessions. |

### Google ADK

| Resource | Summary |
|----------|---------|
| [Google ADK Documentation](https://google.github.io/adk-docs/) | Agent Development Kit - flexible framework for AI agents. Model-agnostic and deployment-agnostic. Supports workflow agents (sequential, parallel, loop), multi-agent architectures, and custom tools. Optimized for Gemini but broadly applicable. |

---

## Pattern-Specific Resources

### Prompt Chaining

| Resource | Summary |
|----------|---------|
| [Red Hat - Responses API Deep Dive](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack) | Deep dive into using Responses API with LlamaStack. Key quote: "Because Llama Stack implements the OpenAI-compatible Responses API, you can use it as a drop-in replacement for a proprietary endpoint." Covers model freedom, data sovereignty, and avoiding vendor lock-in. |
| [Red Hat - Migrating to Responses API](https://developers.redhat.com/articles/2025/12/09/your-ai-agents-evolved-modernize-llama-stack-agents-migrating-responses-api) | Why LlamaStack deprecated legacy Agents API. Benefits: simplified orchestration (no manual lifecycle management), built-in multi-step reasoning, industry alignment. Migration is "an opportunity to simplify your code, improve agent capabilities, and position your system for future innovations." |
| [ODH Agents - Migration Notebook](https://github.com/opendatahub-io/agents/blob/main/migration/legacy-agents/responses-api-agent-migration.ipynb) | Practical Jupyter notebook showing step-by-step migration from legacy Agent APIs to Responses API. Includes side-by-side code examples, National Parks Service tools demo. Shows how new API eliminates need to pre-register tools. |

---

## Real-World Examples

### Production Implementations

| Resource | Summary |
|----------|---------|
| [ODH Dashboard gen-ai BFF](https://github.com/opendatahub-io/odh-dashboard/tree/main/packages/gen-ai/bff) | Production Go backend using LlamaStack Responses API. Shows real-world usage of `Responses.New()` and `Responses.NewStreaming()`. Good reference for enterprise LlamaStack integration. |
| [OpenDataHub - Working with LlamaStack](https://opendatahub.io/docs/working-with-llama-stack/) | Official ODH guide for LlamaStack integration. Covers setup, configuration, and deployment in OpenShift environment. |

### Integration Guides

| Resource | Summary |
|----------|---------|
| [LangChain Integration Guide for Llama](https://www.llama.com/docs/integration-guides/langchain/) | Official Meta guide for using LangChain with Llama models. Shows how to combine LangChain's orchestration with Llama's model capabilities. |
| [Getting Started with Llama Stack - Niklas Heidloff](https://heidloff.net/article/llama-stack/) | Practical getting-started guide. Covers running LlamaStack on desktop machines, basic configuration, and first API calls. Good for beginners. |

---

## By Topic

### Infrastructure vs Orchestration

Understanding the difference between infrastructure layers (LlamaStack) and orchestration frameworks (LangChain, ADK):

- [LlamaStack GitHub](https://github.com/llamastack/llama-stack) - "Composable building blocks"
- [LangChain Docs](https://python.langchain.com/docs/) - "Orchestration framework"
- [IBM - What is LangGraph?](https://www.ibm.com/think/topics/langgraph) - Explains graph-based orchestration

### Model Freedom & Data Sovereignty

Resources about avoiding vendor lock-in:

- [Red Hat - Responses API Deep Dive](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack)
- [LlamaStack Docs](https://llamastack.github.io/docs) - Provider flexibility
- [OpenAI - Responses API](https://developers.openai.com/blog/responses-api/) - The API standard LlamaStack implements

### Migration & Modernization

Resources for updating existing agent implementations:

- [Red Hat - Migrating to Responses API](https://developers.redhat.com/articles/2025/12/09/your-ai-agents-evolved-modernize-llama-stack-agents-migrating-responses-api)
- [ODH Migration Notebook](https://github.com/opendatahub-io/agents/blob/main/migration/legacy-agents/responses-api-agent-migration.ipynb)
