ollama start
ollama run llama3.2:3b --keepalive 60m

 Install uv and start Ollama
ollama run llama3.2:3b --keepalive 60m

# Run Llama Stack server
OLLAMA_URL=http://localhost:11434 \
  uv run --with llama-stack \
  llama stack build --distro starter \
  --image-type venv --run

# Try the Python SDK
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(
  base_url="http://localhost:8321"
)

response = client.chat.completions.create(
  model="Llama3.2-3B-Instruct",
  messages=[{
    "role": "user",
    "content": "What is machine learning?"
  }]
)

Next 
https://rh-aiservices-bu.github.io/llama-stack-tutorial/modules/elementary-02.html