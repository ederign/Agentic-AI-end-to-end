# Agentic Design Patterns: A Framework Comparison

> **Note:** This documentation series was created through collaborative exploration with Claude (Anthropic).

This documentation series explores agentic AI design patterns and compares their implementation across three frameworks:

- **LangChain/LangGraph** - Orchestration framework with rich abstractions
- **LlamaStack** - Infrastructure layer with OpenAI-compatible APIs
- **ADK (Agent Development Kit)** - Google's agent development framework

## Pattern Index

| # | Pattern | Description | Status |
|---|---------|-------------|--------|
| 0 | [Introduction](./00-introduction/) | Framework overview and positioning | Done |
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
        ├── raw.py      # LlamaStack Responses API
        ├── langchain.py # LangChain + LlamaStack
        ├── adk.py      # ADK + LiteLLM
        └── run.py      # Unified CLI
```

## Running Patterns

```bash
# Start LlamaStack (required for raw and langchain)
make llama-server

# Run prompt chaining with different approaches
make prompt-chaining-raw       # Raw LlamaStack
make prompt-chaining-langchain # LangChain + LlamaStack
make prompt-chaining-adk       # ADK
make prompt-chaining-all       # Compare all three
```

## Resources

See [links/](./links/) for a curated bibliography with summaries of all referenced resources, organized by:
- Core Concepts (Responses API, Agentic Patterns)
- Framework Documentation (LlamaStack, LangChain, ADK)
- Pattern-Specific Resources
- Real-World Examples

## Key Insight

Each framework serves a different purpose:

| Framework | Role | Best For |
|-----------|------|----------|
| **LlamaStack** | Infrastructure layer | Model freedom, data sovereignty, unified API |
| **LangChain** | Orchestration layer | Complex workflows, rich abstractions |
| **ADK** | Orchestration layer | Google ecosystem, structured agents |

For complex patterns, consider **LangChain on top of LlamaStack** to get both model freedom and rich orchestration.
