# Agentic Design Patterns

Implementations of agentic design patterns using three approaches:

1. **Raw** - LlamaStack Responses API (no orchestration framework)
2. **LangChain** - LangChain + LlamaStack backend
3. **ADK** - Google's ADK with LiteLLM infrastructure

## Usage

```bash
# Run prompt chaining with different approaches
make prompt-chaining-raw       # Raw LlamaStack
make prompt-chaining-langchain # LangChain + LlamaStack
make prompt-chaining-adk       # ADK

# Run all three for comparison
make prompt-chaining-all

# Or use the CLI directly
uv run --package patterns prompt-chaining --approach raw
uv run --package patterns prompt-chaining --approach langchain
uv run --package patterns prompt-chaining --approach adk
```

## Prerequisites

- For `raw` and `langchain` approaches: Start LlamaStack server with `make llama-server`
- For `adk` approach: Just needs `OPENAI_API_KEY` in `.env`
