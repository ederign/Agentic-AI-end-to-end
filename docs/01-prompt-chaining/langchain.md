# Prompt Chaining: LangChain + LlamaStack

## Approach

LangChain uses **LCEL (LangChain Expression Language)** to compose chains declaratively using the `|` operator.

## Key Concepts

- **ChatPromptTemplate** - Defines prompt templates with variables
- **StrOutputParser** - Converts LLM output to string
- **LCEL Pipe (`|`)** - Chains components together
- **Dictionary mapping** - Passes outputs to named variables

## Implementation

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:8321/v1",  # LlamaStack
    api_key="none",
    model="openai/gpt-4o-mini",
    temperature=0,
)

# Step 1: Extract specifications
prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)

# Step 2: Transform to JSON
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with "
    "'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

# Build chain using LCEL
extraction_chain = prompt_extract | llm | StrOutputParser()

full_chain = (
    {"specifications": extraction_chain}  # Output becomes 'specifications' variable
    | prompt_transform
    | llm
    | StrOutputParser()
)

# Execute
result = full_chain.invoke({"text_input": "The laptop has 16GB RAM..."})
```

## Strengths

- **Declarative syntax** - Easy to read and understand flow
- **Automatic data passing** - LCEL handles variable mapping
- **Composable** - Chains can be nested and combined
- **Streaming support** - Built-in streaming capabilities
- **Debugging** - Verbose mode with callbacks

## Weaknesses

- **Framework lock-in** - Code tied to LangChain abstractions
- **Magic behavior** - Data flow can be non-obvious for complex chains
- **Learning curve** - Need to understand LCEL semantics

## Code Location

`packages/patterns/src/patterns/prompt_chaining/langchain.py`

## Running

```bash
make prompt-chaining-langchain
# or
uv run --package patterns prompt-chaining --approach langchain
```
