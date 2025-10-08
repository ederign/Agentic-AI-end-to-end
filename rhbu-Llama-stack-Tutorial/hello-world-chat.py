from llama_stack_client import LlamaStackClient


client = LlamaStackClient(base_url="http://localhost:8321")

# Define the model ID
model_id = "llama3.2:3b"

while True:
    prompt = input("You: ")
    if prompt.lower() in {"exit", "quit"}:
        break
    response = client.inference.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        model_id=model_id
    )
    print("Llama:", response.completion_message.content)