# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research repository exploring agentic AI patterns using modern Python (3.12+). Uses [uv](https://docs.astral.sh/uv/) for package management with a workspace-based monorepo structure.

**Note:** Eder is learning Python. Always use the most **Pythonic** approach - prefer simple, readable, idiomatic Python over clever or complex patterns. Explain Python concepts when they come up.

## Commands

ALWAYS use `uv` for package management. NEVER use `pip` directly.

### Running patterns
```bash
# Start LlamaStack server first (required for raw and langchain approaches)
make llama-server

# Run prompt chaining with different approaches
make prompt-chaining-raw       # Raw LlamaStack Responses API
make prompt-chaining-langchain # LangChain + LlamaStack
make prompt-chaining-adk       # ADK (uses LiteLLM, no LlamaStack needed)
make prompt-chaining-all       # Compare all three
```

### Adding dependencies to a package
```bash
uv add --package <package_name> <dependency>
```

### Linting and type checking
```bash
uv run ruff check .
uv run pyright
```

### Running tests
```bash
uv run pytest
```

## Architecture

### Workspace Structure
```
├── config/                      # Configuration files
│   └── llamastack-run.yaml      # LlamaStack server config
├── docs/                        # Documentation
├── packages/
│   ├── common/                  # Shared utilities
│   └── patterns/                # All pattern implementations
│       └── prompt_chaining/
│           ├── raw.py           # LlamaStack Responses API
│           ├── langchain.py     # LangChain + LlamaStack
│           ├── adk.py           # ADK + LiteLLM
│           └── run.py           # Unified CLI
```

### Three Approaches for Each Pattern
1. **Raw** - LlamaStack Responses API directly (no orchestration framework)
2. **LangChain** - LangChain with LlamaStack as backend
3. **ADK** - Google ADK with its own infrastructure (LiteLLM)

### Pattern Organization
Patterns are organized under `packages/patterns/src/patterns/<pattern_name>/`:
- `raw.py` - Direct LlamaStack Responses API implementation
- `langchain.py` - LangChain implementation (uses LlamaStack backend)
- `adk.py` - ADK implementation (uses LiteLLM)
- `run.py` - Unified CLI entry point with `--approach` flag

### Environment Configuration
API keys are loaded from `.env` at repository root using `common.env.load_repo_dotenv()`. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`.

## Implementation Notes

### LlamaStack
When implementing patterns with LlamaStack, use the OpenAI client in this priority order:
1. **Responses API** (`client.responses.create`) - preferred, use this by default
2. **Chat Completions API** (`client.chat.completions.create`) - fallback if Responses API doesn't support a feature
3. **LlamaStack client** - requires explicit approval from Eder first

Do NOT use the LlamaStack client directly without asking Eder.

### LangChain
When using LangChain, always configure it to use LlamaStack as the backend:
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:8321/v1",  # LlamaStack
    api_key="none",
    model="openai/gpt-4o-mini",
)
```

### ADK
ADK uses LiteLLM internally as its infrastructure layer. It does NOT use LlamaStack - this is intentional to show ADK as a complete alternative solution.

## Documentation Requirements

**IMPORTANT:** When making structural changes, adding new patterns, or modifying code:

1. **Always review and update documentation:**
   - `README.md` - Root project overview
   - `docs/README.md` - Main documentation index
   - `docs/<pattern>/` - Pattern-specific documentation

2. **For new patterns, create:**
   - `docs/XX-pattern-name/README.md` - Pattern overview
   - `docs/XX-pattern-name/raw.md` - Raw approach docs
   - `docs/XX-pattern-name/langchain.md` - LangChain approach docs
   - `docs/XX-pattern-name/adk.md` - ADK approach docs
   - `docs/XX-pattern-name/comparison.md` - Side-by-side comparison

3. **Update code locations and commands** in docs when moving files or changing CLI.

4. **When adding utilities to `common` package**, update `packages/common/README.md` with the new function/module.
