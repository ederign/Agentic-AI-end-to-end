# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research repository exploring agentic AI patterns using modern Python (3.12+). Uses [uv](https://docs.astral.sh/uv/) for package management with a workspace-based monorepo structure.

## Commands

### Running examples
```bash
uv run --package langchain_impl prompt-chaining
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
- `packages/common/` - Shared utilities (env loading from repo root `.env`)
- `packages/langchain_impl/` - LangChain/LangGraph implementations
- `packages/llamastack_impl/` - LlamaStack implementations (planned)
- `packages/adk_impl/` - ADK implementations (planned)

Each package follows the `src/<package_name>/` layout and depends on `common` via workspace reference.

### Pattern Organization
Agentic patterns are organized under `packages/<impl>/src/<impl>/patterns/<pattern_name>/`:
- `chain.py` - Core pattern logic
- `run.py` - Entry point with `main()` function (registered as script in pyproject.toml)

### Environment Configuration
API keys are loaded from `.env` at repository root using `common.env.load_repo_dotenv()`. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`.

## Implementation Notes

### LlamaStack
When implementing patterns with LlamaStack, prefer using the OpenAI Responses API client when possible for consistency and simplicity.
