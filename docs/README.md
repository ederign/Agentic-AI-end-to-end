# Agentic Design Patterns: An Approach Comparison

> **Repository:** [github.com/ederign/Agentic-AI-end-to-end](https://github.com/ederign/Agentic-AI-end-to-end)
> **Note:** These findings emerged from collaborative exploration with Claude (Anthropic), including hands-on implementation and documentation research.

Two of my main goals for this year are to learn **Agentic AI end-to-end** and to embrace **AI assistance** in my daily life—both in coding and in studying. With that in mind, I decided to start this blog series based on the book **"Agentic Design Patterns"** by **Antonio Gullí**, using Claude as my research companion throughout the process.


## What Are Agentic Design Patterns?

Agentic design patterns are reusable architectural approaches for building AI applications that go beyond simple prompt-response interactions. These patterns enable:

- **Multi-step reasoning** - Breaking complex tasks into manageable steps
- **Tool usage** - Integrating external capabilities (search, APIs, databases)
- **Self-correction** - Evaluating and improving outputs
- **Autonomous workflows** - Coordinating multiple AI components

## The Three Approaches

This documentation series explores agentic AI design patterns and compares their implementation across three approaches:

- **OpenAI APIs** - OpenAI-compatible APIs (Responses/Completions) with LlamaStack as infrastructure
- **LangChain** - LangChain for orchestration with LlamaStack as infrastructure
- **ADK** - Google's Agent Development Kit with LiteLLM as infrastructure

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Code                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              Orchestration Layer (choose one)               │
│                                                             │
│   ┌──────────────┐  ┌──────────────┐    ┌──────────────┐    │
│   │  LangChain   │  │     ADK      │    │  Manual Code │    │
│   │              │  │              │    │(OpenAI APIs) │    │
│   └──────────────┘  └──────────────┘    └──────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │ OpenAI-compatible API
┌─────────────────────────▼───────────────────────────────────┐
│                   Infrastructure Layer                      │
│                                                             │
│   ┌────────────────────────┐  ┌────────────────────────┐    │
│   │       LlamaStack       │  │        LiteLLM         │    │
│   │  (OpenAI APIs +        │  │        (ADK)           │    │
│   │   LangChain)           │  │                        │    │
│   └────────────────────────┘  └────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Model Providers                          │
│                                                             │
│   OpenAI  │  vLLM  │  Ollama  │  TGI  │  Anthropic  │  ...  │
└─────────────────────────────────────────────────────────────┘
```

### Approach Comparison

| Approach | Orchestration | Infrastructure | Best For |
|----------|---------------|----------------|----------|
| **OpenAI APIs** | Manual | LlamaStack | Learning fundamentals, full control |
| **LangChain** | LangChain/LCEL | LlamaStack | Complex workflows, rich abstractions |
| **ADK** | Google ADK | LiteLLM | Structured agents, multi-agent systems |

LlamaStack provides model freedom and data sovereignty. LangChain on top of LlamaStack gives you both rich orchestration and infrastructure flexibility. ADK offers a structured, agent-first approach with LiteLLM providing similar model flexibility.

## Pattern Index

| # | Pattern | Description | Status |
|---|---------|-------------|--------|
| 1 | [Prompt Chaining](./01-prompt-chaining/) | Sequential prompt execution with output passing | Done |
| 2 | Routing | Coming soon | Planned |
| 3 | Parallelization | Coming soon | Planned |
| 4 | Orchestrator-Workers | Coming soon | Planned |
| 5 | Evaluator-Optimizer | Coming soon | Planned |

## Repository Structure

```
packages/
├── common/             # Shared utilities
└── patterns/           # All pattern implementations
    └── prompt_chaining/
        ├── raw.py      # OpenAI APIs (Responses/Completions)
        ├── langchain.py # LangChain + LlamaStack
        ├── adk.py      # ADK + LiteLLM
        └── run.py      # Unified CLI
```

## Running Patterns

```bash
# Start LlamaStack (required for OpenAI APIs and LangChain approaches)
make llama-server

# Run prompt chaining with different approaches
make prompt-chaining-raw       # OpenAI APIs
make prompt-chaining-langchain # LangChain + LlamaStack
make prompt-chaining-adk       # ADK
make prompt-chaining-all       # Compare all three
```

## Resources

See [links/](./links/) for a curated bibliography with summaries of all referenced resources.

## References

- [Agentic Design Patterns](https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018) by Antonio Gullí - The book that serves as the basis for this project
- [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [LlamaStack GitHub](https://github.com/llamastack/llama-stack)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
