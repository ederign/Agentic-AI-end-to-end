# Pattern 1: Prompt Chaining

> **Note:** These findings emerged from collaborative exploration with Claude (Anthropic), including hands-on implementation and documentation research.

## What is Prompt Chaining?

Prompt chaining is the simplest agentic pattern: a sequence of LLM calls where the output of one step becomes the input for the next. It's the foundation for more complex patterns.

```
Input → [Prompt 1] → Output₁ → [Prompt 2] → Output₂ → ... → Final Result
```

## Use Cases

- **Data extraction and transformation** - Extract info → Clean → Format
- **Multi-stage reasoning** - Analyze → Critique → Refine
- **Content generation pipelines** - Outline → Draft → Edit → Polish
- **Validation workflows** - Generate → Validate → Fix if needed

## Our Example: Specs Extraction

All three implementations solve the same problem:

```
Input: "The laptop has a 3.5 GHz octa-core processor, 16GB RAM, and 1TB NVMe SSD"
     ↓
[Step 1: Extract] → Bullet points of specs
     ↓
[Step 2: Transform] → Structured JSON
     ↓
Output: {"cpu": "3.5 GHz octa-core", "memory": "16GB", "storage": "1TB NVMe SSD"}
```

## Approach Comparison

| Aspect | Raw (LlamaStack) | LangChain | ADK |
|--------|------------------|-----------|-----|
| **Infrastructure** | LlamaStack | LlamaStack | LiteLLM |
| **Orchestration** | Manual | LCEL chains | SequentialAgent |
| **Lines of code** | ~40 | ~25 | ~70 |
| **Data passing** | Manual variable passing | Automatic via LCEL | State dictionary |
| **Boilerplate** | Low | Low | Medium |
| **Type safety** | Pydantic | Optional | Pydantic + output_schema |

## Implementation Details

See individual approach documentation:
- [Raw (LlamaStack Responses API)](./raw.md)
- [LangChain + LlamaStack](./langchain.md)
- [ADK](./adk.md)

## Summary Comparison

See [comparison.md](./comparison.md) for detailed side-by-side analysis.
