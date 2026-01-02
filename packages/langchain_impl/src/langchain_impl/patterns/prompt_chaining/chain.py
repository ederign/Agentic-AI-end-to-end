from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_prompt_chaining(text_input: str) -> str:
    chain = build_chain(text_input)
    # Execute the chain with the input text dictionary.
    return chain.invoke({"text_input": text_input})
    
def build_chain(text_input: str) -> str :
    # Code extracted from: https://colab.research.google.com/drive/15XCzDOvBhIQaZ__xkvruf5sP9OznAbK9

    # Initialize the Language Model (using ChatOpenAI is recommended)
    llm = ChatOpenAI(temperature=0)

    # --- Prompt 1: Extract Information ---
    prompt_extract = ChatPromptTemplate.from_template(
        "Extract the technical specifications from the following text:\n\n{text_input}"
    )

    # --- Prompt 2: Transform to JSON ---
    prompt_transform = ChatPromptTemplate.from_template(
        "Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
    )

    # --- Build the Chain using LCEL ---
    # The StrOutputParser() converts the LLM's message output to a simple string.
    extraction_chain = prompt_extract | llm | StrOutputParser()

    # The full chain passes the output of the extraction chain into the 'specifications'
    # variable for the transformation prompt.
    full_chain = (
        {"specifications": extraction_chain}
        | prompt_transform
        | llm
        | StrOutputParser()
    )

    return full_chain