# Pattern 1: Prompt Chaining

> **Repository:** [github.com/ederign/Agentic-AI-end-to-end](https://github.com/ederign/Agentic-AI-end-to-end)
>
> **Note:** These findings emerged from collaborative exploration with Claude (Anthropic), including hands-on implementation and documentation research.

## What is Prompt Chaining?

Prompt chaining is the simplest agentic pattern: a sequence of LLM calls where the output of one step becomes the input for the next. It's the foundation for more complex patterns.

```
Input → [Prompt 1] → Output₁ → [Prompt 2] → Output₂ → ... → Final Result
```

## Why Prompt Chaining?

While a single, detailed prompt can work for simpler tasks, complex workflows benefit from breaking work into sequential steps. This **divide-and-conquer** approach offers several advantages:

- **Simpler prompts** - Each step has a focused, well-defined task
- **Easier debugging** - You can inspect intermediate outputs between steps
- **Better accuracy** - Smaller, focused prompts tend to produce more reliable results
- **Structured outputs** - Each step can enforce specific output formats (JSON, bullet points, etc.)

Prompt chaining is particularly effective when tasks have clear sequential dependencies—where Step 2 genuinely needs the output of Step 1 to proceed.

## Use Cases

- **Data extraction and transformation** - Extract info → Clean → Format
- **Multi-stage reasoning** - Analyze → Critique → Refine
- **Content generation pipelines** - Outline → Draft → Edit → Polish
- **Validation workflows** - Generate → Validate → Fix if needed

## Our Example: Specs Extraction

This example is adapted from the book's prompt chaining chapter. All three implementations solve the same problem:

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

## References

- **Agentic Design Patterns** by Antonio Gullí - The book that serves as the basis for this project
- [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
