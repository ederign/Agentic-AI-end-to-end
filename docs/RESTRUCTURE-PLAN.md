# Restructure Plan: Three Approaches to Agentic Patterns

> **Status:** Planning (to be implemented)
> **Created:** During collaborative session with Claude

## The Core Idea

For each agentic pattern, show **3 complete, independent approaches**:

```
┌─────────────────────────────────────────────────────────────────┐
│                      For Each Pattern                           │
├─────────────────┬─────────────────────┬─────────────────────────┤
│   Approach 1    │     Approach 2      │      Approach 3         │
├─────────────────┼─────────────────────┼─────────────────────────┤
│   Raw           │  LangChain          │   ADK                   │
│   LlamaStack    │  + LlamaStack       │   (own infra)           │
│   Responses API │  as backend         │   via LiteLLM           │
├─────────────────┼─────────────────────┼─────────────────────────┤
│      ↓          │        ↓            │         ↓               │
│   OpenAI/       │   OpenAI/           │   OpenAI/               │
│   Ollama/vLLM   │   Ollama/vLLM       │   Anthropic/Gemini      │
└─────────────────┴─────────────────────┴─────────────────────────┘
```

## Why This Structure?

| Approach | What It Demonstrates | Trade-offs |
|----------|---------------------|------------|
| **Raw LlamaStack** | "Build it yourself" - understand fundamentals, maximum control | Most control, least abstraction, model freedom |
| **LangChain + LlamaStack** | "Rich orchestration" - abstractions + model freedom | Rich abstractions, state management, more dependencies |
| **ADK** | "Google's way" - opinionated, batteries-included | Structured, but tied to LiteLLM infrastructure |

### Key Insight: ADK Is a Different Path

ADK uses **LiteLLM** internally as its infrastructure layer. Stacking ADK on LlamaStack would be redundant (two gateway layers). Instead, we show ADK as a **complete alternative solution** with its own infrastructure.

This gives readers an honest comparison of three complete approaches, not a forced attempt to make everything use the same backend.

## Pattern Catalog (From Book Outline)

### Part One: Core Patterns (103 pages)

| # | Pattern | Description |
|---|---------|-------------|
| 1 | **Prompt Chaining** | Sequential prompts where output feeds into the next |
| 2 | **Routing** | Dynamic path selection based on input characteristics |
| 3 | **Parallelization** | Concurrent execution of independent tasks |
| 4 | **Reflection** | Self-evaluation and improvement loops |
| 5 | **Tool Use** | Integrating external capabilities |
| 6 | **Planning** | Breaking complex tasks into steps |
| 7 | **Multi-Agent** | Coordinating multiple specialized agents |

### Part Two: State & Context (61 pages)

| # | Pattern | Description |
|---|---------|-------------|
| 8 | **Memory Management** | Short-term and long-term memory |
| 9 | **Learning and Adaptation** | Improving from experience |
| 10 | **Model Context Protocol (MCP)** | Standardized context sharing |
| 11 | **Goal Setting and Monitoring** | Objective tracking |

### Part Three: Reliability (34 pages)

| # | Pattern | Description |
|---|---------|-------------|
| 12 | **Exception Handling and Recovery** | Graceful failure handling |
| 13 | **Human-in-the-Loop** | Human oversight integration |
| 14 | **Knowledge Retrieval (RAG)** | Retrieval-augmented generation |

### Part Four: Advanced (114 pages)

| # | Pattern | Description |
|---|---------|-------------|
| 15 | **Inter-Agent Communication (A2A)** | Agent-to-agent protocols |
| 16 | **Resource-Aware Optimization** | Efficiency and cost management |
| 17 | **Reasoning Techniques** | Chain-of-thought, tree-of-thought |
| 18 | **Guardrails/Safety Patterns** | Content filtering, safety shields |
| 19 | **Evaluation and Monitoring** | Measuring agent performance |
| 20 | **Prioritization** | Task and resource prioritization |
| 21 | **Exploration and Discovery** | Autonomous exploration |

### Appendices (74 pages)

| # | Topic |
|---|-------|
| A | Advanced Prompting Techniques |
| B | AI Agentic: From GUI to Real World |
| C | Quick Overview of Agentic Frameworks |
| D | Building an Agent with AgentSpace |
| E | AI Agents on the CLI |
| F | Under the Hood: Agents' Reasoning Engines |
| G | Coding Agents |

## Chapter Template

Each pattern chapter follows this structure:

```markdown
## Chapter N: [Pattern Name]

### What Is This Pattern?
Brief explanation, when to use it, real-world examples

### Approach 1: Raw (LlamaStack Responses API)

```python
# Implementation using direct Responses API calls
```

**Pros:** Full control, minimal dependencies, understand every step
**Cons:** More code for complex patterns, no built-in state management

### Approach 2: LangChain + LlamaStack

```python
# Implementation using LCEL or LangGraph
# LlamaStack as the backend (base_url="http://localhost:8321/v1")
```

**Pros:** Rich abstractions, state management, model freedom
**Cons:** Learning curve, more dependencies

### Approach 3: ADK

```python
# Implementation using Google's ADK
# Uses its own infrastructure (LiteLLM)
```

**Pros:** Structured agents, Google ecosystem integration
**Cons:** Tied to LiteLLM, less model flexibility

### Comparison

| Aspect | Raw | LangChain | ADK |
|--------|-----|-----------|-----|
| Lines of code | X | Y | Z |
| Dependencies | minimal | langchain, langgraph | google-adk |
| Model freedom | High | High | Medium |
| State management | Manual | Built-in | Built-in |
| Learning curve | Low | Medium | Medium |

### When to Use Each

- **Raw:** When you need full control or are learning the fundamentals
- **LangChain:** When you need rich orchestration + want model freedom
- **ADK:** When you're in the Google ecosystem or prefer structured agents
```

## Project Structure

### Recommended: Single Package with Sub-modules

```
packages/
├── common/                          # Shared utilities (keep)
└── patterns/                        # All patterns here
    ├── pyproject.toml
    └── src/patterns/
        ├── __init__.py
        ├── prompt_chaining/
        │   ├── __init__.py
        │   ├── raw.py               # LlamaStack Responses API
        │   ├── langchain.py         # LangChain + LlamaStack
        │   ├── adk.py               # ADK (own infrastructure)
        │   └── run.py               # CLI: choose approach
        ├── routing/
        │   ├── raw.py
        │   ├── langchain.py
        │   ├── adk.py
        │   └── run.py
        └── ... (other patterns)
```

### Documentation Structure

```
docs/
├── README.md                        # Main index
├── 00-introduction/
│   ├── README.md                    # What are agentic patterns?
│   ├── frameworks-overview.md       # LlamaStack vs LangChain vs ADK
│   └── infrastructure-comparison.md # LlamaStack vs LiteLLM vs Portkey
├── 01-prompt-chaining/
│   ├── README.md                    # Pattern overview
│   ├── raw.md                       # Raw approach
│   ├── langchain.md                 # LangChain approach
│   ├── adk.md                       # ADK approach
│   └── comparison.md                # Side-by-side
├── 02-routing/
│   └── ...
├── ... (patterns 3-21)
├── appendices/
│   ├── a-prompting-techniques.md
│   ├── b-gui-to-real-world.md
│   └── ...
├── links/
│   └── README.md                    # Bibliography
└── RESTRUCTURE-PLAN.md              # This file
```

## Implementation Approach

### Approach 1: Raw LlamaStack

Uses LlamaStack's Responses API directly:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8321/v1",
    api_key="none"
)

response = client.responses.create(
    model="openai/gpt-4o-mini",
    input="Your prompt here"
)
result = response.output_text
```

### Approach 2: LangChain + LlamaStack

Uses LangChain with LlamaStack as backend:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:8321/v1",
    api_key="none",
    model="openai/gpt-4o-mini"
)

# Use LCEL or LangGraph for orchestration
chain = prompt | llm | parser
result = chain.invoke({"input": "..."})
```

### Approach 3: ADK

Uses ADK with its built-in LiteLLM infrastructure:

```python
from google.adk.agents import SequentialAgent
from google.adk.models import LiteLLM

model = LiteLLM(model="openai/gpt-4o-mini")
agent = SequentialAgent(
    name="my_agent",
    model=model,
    steps=[step1, step2, step3]
)
result = agent.run(input_data)
```

## The Educational Story

> "This book shows you 3 ways to implement each agentic pattern:
>
> 1. **Build it yourself** with LlamaStack's Responses API - understand every step
> 2. **Use LangChain** on top of LlamaStack - rich orchestration + model freedom
> 3. **Use Google's ADK** - a complete alternative with its own infrastructure
>
> Each approach has trade-offs. Choose based on your constraints."

## Prerequisites Before Starting

- [ ] Verify LangChain works with LlamaStack backend (confirmed works)
- [ ] Set up ADK development environment
- [ ] Create new `patterns` package structure
- [ ] Update Makefile for new structure
- [ ] Clean up old package structure

## References

- LlamaStack: Infrastructure layer, "drop-in replacement for proprietary endpoints"
- LangChain: Orchestration framework, works with custom base URLs
- ADK: Google's agent framework, uses LiteLLM internally
- Our discussion: ADK + LlamaStack is redundant (two gateway layers)
