# ABOUTME: Prompt chaining using LangChain with LlamaStack as the backend.
# ABOUTME: Demonstrates LCEL (LangChain Expression Language) for composable pipelines.

from langchain_core.callbacks import StdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

# LlamaStack server endpoint (started via `make llama-server`)
LLAMASTACK_BASE_URL = "http://localhost:8321/v1"
MODEL = "openai/gpt-4o-mini"


def run_prompt_chaining(text_input: str, verbose: bool = False) -> str:
    """Run the prompt chaining pipeline and return result."""
    chain = build_chain()
    config: RunnableConfig | None = (
        {"callbacks": [StdOutCallbackHandler()]} if verbose else None
    )
    return chain.invoke({"text_input": text_input}, config=config)


def build_chain() -> Runnable:
    """Build the prompt chaining pipeline using LCEL."""

    # Initialize the Language Model using LlamaStack as the backend
    llm = ChatOpenAI(
        base_url=LLAMASTACK_BASE_URL,
        api_key=SecretStr("none"),
        model=MODEL,
        temperature=0,
    )

    # --- Prompt 1: Extract Information ---
    prompt_extract = ChatPromptTemplate.from_template(
        "Extract the technical specifications from the following text:\n\n{text_input}"
    )

    # --- Prompt 2: Transform to JSON ---
    prompt_transform = ChatPromptTemplate.from_template(
        "Transform the following specifications into a JSON object with "
        "'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
    )

    # --- Build the Chain using LCEL ---
    extraction_chain = prompt_extract | llm | StrOutputParser()

    full_chain = (
        {"specifications": extraction_chain}
        | prompt_transform
        | llm
        | StrOutputParser()
    )

    return full_chain
