# Agentic AI End-to-End

Research repository exploring agentic AI design patterns with three implementation approaches.

## Quick Start

```bash
# Start LlamaStack server (required for raw and langchain approaches)
make llama-server

# Run prompt chaining pattern
make prompt-chaining-raw       # Raw LlamaStack Responses API
make prompt-chaining-langchain # LangChain + LlamaStack
make prompt-chaining-adk       # Google ADK

# Compare all three
make prompt-chaining-all
```

## The Three Approaches

| Approach | Infrastructure | Orchestration | Best For |
|----------|---------------|---------------|----------|
| **Raw** | LlamaStack | None (manual) | Learning fundamentals, full control |
| **LangChain** | LlamaStack | LangChain/LCEL | Rich abstractions + model freedom |
| **ADK** | LiteLLM | Google ADK | Structured agents, Google ecosystem |

## Documentation

See [docs/](./docs/) for detailed documentation including:

- [Introduction & Framework Overview](./docs/00-introduction/)
- [Pattern Implementations](./docs/01-prompt-chaining/)
- [Bibliography & References](./docs/links/)

## Project Structure

```
├── config/                  # Configuration files
│   └── llamastack-run.yaml  # LlamaStack server config
├── docs/                    # Documentation
└── packages/
    ├── common/              # Shared utilities
    └── patterns/            # Pattern implementations
        └── prompt_chaining/
            ├── raw.py       # LlamaStack Responses API
            ├── langchain.py # LangChain + LlamaStack
            ├── adk.py       # Google ADK
            └── run.py       # Unified CLI
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for package management
- OpenAI API key in `.env`

## Setup

```bash
# Install dependencies
uv sync

# Setup git hooks (runs lint + typecheck before each commit)
make setup-hooks
```

## Code Quality

```bash
make lint       # Run ruff linter
make typecheck  # Run pyright type checker
make check      # Run both (also runs automatically on commit)
```
