import asyncio
import json

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.runners import InMemoryRunner
from google.genai import types
from pydantic import BaseModel, Field


# Initialize the Language Model (using OpenAI via LiteLLM)
MODEL = "openai/gpt-4o-mini"


class SpecsJson(BaseModel):
    """Output schema for structured JSON response."""

    cpu: str = Field(description="CPU model / cores / relevant CPU details")
    memory: str = Field(description="RAM size (and relevant details)")
    storage: str = Field(description="Storage size/type (SSD/HDD/NVMe, etc.)")


def run_prompt_chaining(text_input: str, verbose: bool = False) -> str:
    """Run the prompt chaining pipeline and return JSON string result."""
    result = asyncio.run(_run_async(text_input, verbose))
    return result.model_dump_json(indent=2)


def build_agent() -> SequentialAgent:
    """Build the prompt chaining pipeline using ADK SequentialAgent."""

    # --- Step 1: Extract Information ---
    extract_agent = LlmAgent(
        name="extract_specs_agent",
        model=MODEL,
        instruction=(
            "Extract the technical specifications from the following text:\n\n"
            "{user_text}\n\n"
            "Return only the extracted specs as concise bullet points."
        ),
        generate_content_config=types.GenerateContentConfig(temperature=0),
        include_contents="none",
        output_key="specifications",
    )

    # --- Step 2: Transform to JSON ---
    transform_agent = LlmAgent(
        name="transform_specs_agent",
        model=MODEL,
        instruction=_build_transform_instruction,
        generate_content_config=types.GenerateContentConfig(temperature=0),
        include_contents="none",
        output_schema=SpecsJson,
        output_key="result",
    )

    # --- Build the Pipeline ---
    # SequentialAgent runs sub_agents in order, passing state between them.
    return SequentialAgent(
        name="specs_pipeline",
        sub_agents=[extract_agent, transform_agent],
    )


# --- Private helpers ---


def _build_transform_instruction(ctx: ReadonlyContext) -> str:
    """Build transform instruction by reading extracted specs from state."""
    specs = ctx.state.get("specifications", "")
    return (
        "Transform the following specifications into a JSON object with "
        "'cpu', 'memory', and 'storage' as keys:\n\n"
        f"{specs}"
    )


async def _run_async(text_input: str, verbose: bool) -> SpecsJson:
    """Execute the pipeline asynchronously."""
    agent = build_agent()
    runner = InMemoryRunner(agent=agent, app_name="specs_app")

    # Create session with initial state
    await runner.session_service.create_session(
        app_name="specs_app",
        user_id="user",
        session_id="session",
        state={"user_text": text_input},
    )

    # Run the pipeline
    user_message = types.Content(role="user", parts=[types.Part(text=text_input)])
    async for event in runner.run_async(
        user_id="user",
        session_id="session",
        new_message=user_message,
    ):
        if verbose and event.content and event.content.parts:
            print(f"[{event.author}] {event.content.parts[0].text}")

    # Read result from state
    session = await runner.session_service.get_session(
        app_name="specs_app", user_id="user", session_id="session"
    )
    if session is None:
        raise RuntimeError("Session not found")
    result = session.state.get("result", {})
    if isinstance(result, str):
        result = json.loads(result)

    return SpecsJson.model_validate(result)
