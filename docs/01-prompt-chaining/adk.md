# Prompt Chaining: ADK (Google Agent Development Kit)

## Approach

ADK uses **SequentialAgent** to chain multiple **LlmAgent** instances. State is passed between agents via a shared state dictionary.

## Key Concepts

- **LlmAgent** - Individual agent with model, instruction, and output configuration
- **SequentialAgent** - Runs sub-agents in order
- **State dictionary** - Shared context between agents
- **output_key** - Where agent stores its result in state
- **output_schema** - Pydantic model for structured output

## Why Dynamic Instructions? (Lazy Evaluation)

A common question: why pass a **function** for the second agent's instruction instead of just using `{specifications}` in the string?

```python
# ❌ This WON'T work
transform_agent = LlmAgent(
    instruction="Transform: {specifications}"  # specifications doesn't exist at build time!
)

# ✅ This WORKS
transform_agent = LlmAgent(
    instruction=build_transform_instruction  # Called at RUN time
)
```

**The problem is timing:**

| When | What Happens | `state["specifications"]` |
|------|--------------|---------------------------|
| **Build time** | Agents are created | Doesn't exist yet |
| **Run time** | Step 1 executes | Now exists! |
| **Run time** | Step 2 starts, function called | Can read it |

ADK only interpolates `{variables}` from the **initial state** (passed to `create_session`). Values added by previous agents aren't automatically available in template strings.

**The solution:** Pass a function that ADK calls **when the agent runs**, not when it's created:

```python
def build_transform_instruction(ctx: ReadonlyContext) -> str:
    specs = ctx.state.get("specifications", "")  # Read at run time
    return f"Transform to JSON:\n\n{specs}"
```

This "lazy evaluation" pattern is common in many frameworks when you need to access data that doesn't exist yet at configuration time.

## Implementation

```python
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import InMemoryRunner
from pydantic import BaseModel, Field

MODEL = "openai/gpt-4o-mini"

class SpecsJson(BaseModel):
    cpu: str = Field(description="CPU details")
    memory: str = Field(description="RAM size")
    storage: str = Field(description="Storage details")

# Step 1: Extract agent
extract_agent = LlmAgent(
    name="extract_specs_agent",
    model=MODEL,
    instruction=(
        "Extract the technical specifications from the following text:\n\n"
        "{user_text}\n\n"
        "Return only the extracted specs as concise bullet points."
    ),
    output_key="specifications",  # Stores result in state["specifications"]
)

# Step 2: Transform agent
def build_transform_instruction(ctx):
    specs = ctx.state.get("specifications", "")
    return f"Transform to JSON with cpu, memory, storage keys:\n\n{specs}"

transform_agent = LlmAgent(
    name="transform_specs_agent",
    model=MODEL,
    instruction=build_transform_instruction,  # Dynamic instruction from state
    output_schema=SpecsJson,  # Structured output
    output_key="result",
)

# Build pipeline
pipeline = SequentialAgent(
    name="specs_pipeline",
    sub_agents=[extract_agent, transform_agent],
)

# Execute
runner = InMemoryRunner(agent=pipeline, app_name="specs_app")
# ... session setup and execution
```

## Strengths

- **Structured agents** - Clear agent definitions with explicit configuration
- **Type safety** - output_schema with Pydantic validation
- **State management** - Built-in state passing between agents
- **Named outputs** - output_key makes data flow explicit
- **Reusable agents** - Agents can be composed into different pipelines

## Weaknesses

- **More boilerplate** - Async setup, sessions, runners required
- **Complex execution** - Need to manage sessions and async flow
- **State extraction** - Must read results from state after execution
- **Learning curve** - More concepts to understand (agents, runners, sessions)

## Async Execution Pattern

ADK is async-first, requiring explicit async handling:

```python
async def run_pipeline(text_input: str):
    agent = build_agent()
    runner = InMemoryRunner(agent=agent, app_name="app")

    # Create session with initial state
    await runner.session_service.create_session(
        app_name="app",
        user_id="user",
        session_id="session",
        state={"user_text": text_input},
    )

    # Run and stream events
    async for event in runner.run_async(
        user_id="user",
        session_id="session",
        new_message=user_message,
    ):
        print(f"[{event.author}] {event.content}")

    # Extract result from state
    session = await runner.session_service.get_session(...)
    return session.state.get("result")
```

## Code Location

`packages/patterns/src/patterns/prompt_chaining/adk.py`

## Running

```bash
make prompt-chaining-adk
# or
uv run --package patterns prompt-chaining --approach adk
```

## References

- **Agentic Design Patterns** by Antonio Gullí - The book that serves as the basis for this project
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
