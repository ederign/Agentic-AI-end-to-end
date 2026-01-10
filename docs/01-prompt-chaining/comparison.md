# Prompt Chaining: Framework Comparison

> **Note:** These findings emerged from collaborative exploration with Claude (Anthropic).

## Summary Table

| Aspect | LangChain | LlamaStack | ADK |
|--------|-----------|------------|-----|
| **Chaining mechanism** | LCEL (`\|` operator) | Manual API calls | SequentialAgent |
| **Data passing** | Automatic via dict mapping | Manual variable passing | State dictionary |
| **Lines of code** | ~25 | ~40 | ~70 |
| **Boilerplate** | Low | Low | Medium-High |
| **Type safety** | Optional | Pydantic | Pydantic + output_schema |
| **Async required** | No | No | Yes |
| **Framework lock-in** | High | None | Medium |
| **Model portability** | Via integrations | Native (config change) | Via LiteLLM |

## Code Comparison

### LangChain - Declarative Chaining

```python
# Clean, declarative pipeline
extraction_chain = prompt_extract | llm | StrOutputParser()
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)
result = full_chain.invoke({"text_input": input})
```

### LlamaStack - Manual Orchestration

```python
# Explicit API calls
response1 = client.responses.create(model=MODEL, input=prompt1)
specs = response1.output_text

response2 = client.responses.create(model=MODEL, input=f"{prompt2}\n{specs}")
result = response2.output_text
```

### ADK - Agent-Based Pipeline

```python
# Structured agent definitions
extract_agent = LlmAgent(name="extract", instruction=..., output_key="specs")
transform_agent = LlmAgent(name="transform", instruction=..., output_schema=SpecsJson)
pipeline = SequentialAgent(sub_agents=[extract_agent, transform_agent])

# Async execution with session management
async for event in runner.run_async(...):
    ...
result = session.state.get("result")
```

## Key Findings

### LangChain

**Best for:** Teams wanting rapid development with rich abstractions

- LCEL provides elegant, readable pipeline syntax
- Automatic data passing reduces boilerplate
- Rich ecosystem of integrations
- Trade-off: Framework lock-in

### LlamaStack

**Best for:** Teams prioritizing model freedom and data sovereignty

- No orchestration abstractions (that's not its purpose)
- Simple OpenAI-compatible API calls
- Easy to swap model providers via config
- For complex patterns: use LangChain on top
- Key insight: It's an **infrastructure layer**, not orchestration

### ADK

**Best for:** Teams building structured, multi-agent systems

- Explicit agent definitions with clear responsibilities
- Built-in state management between agents
- Good type safety with output_schema
- Trade-off: More boilerplate, async complexity

## Recommendation Matrix

| Scenario | Recommended Approach |
|----------|---------------------|
| Quick prototype | LangChain |
| Production with model flexibility | LangChain + LlamaStack |
| Data sovereignty requirements | LlamaStack (manual or + LangChain) |
| Multi-agent systems | ADK |
| Minimal dependencies | LlamaStack (manual) |
| Google Cloud integration | ADK |

## Complexity vs Flexibility Trade-off

```
                    More Flexibility
                          ↑
                          │
    LlamaStack (manual) ──┼── Most flexible, most code
                          │
              ADK ────────┼── Structured, moderate code
                          │
         LangChain ───────┼── Least code, most abstraction
                          │
                          ↓
                    Less Flexibility
```

## The Hybrid Approach

For production systems needing both rich orchestration AND model freedom:

```python
from langchain_openai import ChatOpenAI

# LlamaStack provides infrastructure
llm = ChatOpenAI(
    base_url="http://localhost:8321/v1",  # LlamaStack
    api_key="none",
    model="openai/gpt-4o-mini"
)

# LangChain provides orchestration
chain = prompt1 | llm | parser | prompt2 | llm
```

**Benefits:**
- Swap models via LlamaStack config (no code changes)
- Rich LangChain abstractions for complex workflows
- Data stays in your infrastructure
- Best of both worlds

## References

- **Agentic Design Patterns** by Antonio Gullí - The book that serves as the basis for this project
- [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Guide to agentic design patterns
- [LlamaStack GitHub](https://github.com/llamastack/llama-stack) - "Composable building blocks to build LLM Apps"
- [LangChain Docs](https://python.langchain.com/docs/)
- [Google ADK Docs](https://google.github.io/adk-docs/)
- [Red Hat - Responses API Deep Dive](https://developers.redhat.com/articles/2025/08/20/your-agent-your-rules-deep-dive-responses-api-llama-stack)
