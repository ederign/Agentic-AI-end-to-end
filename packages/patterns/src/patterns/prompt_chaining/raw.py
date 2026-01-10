# ABOUTME: Prompt chaining using LlamaStack's Responses API directly.
# ABOUTME: No orchestration framework - shows the fundamentals of prompt chaining.

import json

from openai import OpenAI
from pydantic import BaseModel, Field

# LlamaStack server endpoint (started via `make llama-server`)
LLAMASTACK_BASE_URL = "http://localhost:8321/v1"
MODEL = "openai/gpt-4o-mini"


class SpecsJson(BaseModel):
    """Output schema for structured JSON response."""

    cpu: str = Field(description="CPU model / cores / relevant CPU details")
    memory: str = Field(description="RAM size (and relevant details)")
    storage: str = Field(description="Storage size/type (SSD/HDD/NVMe, etc.)")


def run_prompt_chaining(text_input: str, verbose: bool = False) -> str:
    """Run the prompt chaining pipeline and return JSON string result."""
    client = OpenAI(base_url=LLAMASTACK_BASE_URL, api_key="none")

    # --- Step 1: Extract Information ---
    if verbose:
        print("[extract_specs] Extracting technical specifications...")

    extraction_response = client.responses.create(
        model=MODEL,
        input=(
            "Extract the technical specifications from the following text:\n\n"
            f"{text_input}\n\n"
            "Return only the extracted specs as concise bullet points."
        ),
    )
    specifications = extraction_response.output_text

    if verbose:
        print(f"[extract_specs] Result:\n{specifications}\n")

    # --- Step 2: Transform to JSON ---
    if verbose:
        print("[transform_specs] Transforming to structured JSON...")

    transform_response = client.responses.create(
        model=MODEL,
        input=(
            "Transform the following specifications into a JSON object with "
            "'cpu', 'memory', and 'storage' as keys:\n\n"
            f"{specifications}\n\n"
            "Return only valid JSON, no markdown or extra text."
        ),
    )
    json_text = transform_response.output_text

    if verbose:
        print(f"[transform_specs] Result:\n{json_text}\n")

    # Parse and validate with Pydantic
    result = SpecsJson.model_validate(json.loads(json_text))
    return result.model_dump_json(indent=2)
