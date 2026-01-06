## LlamaStack Server

### Prerequisites
- OPENAI_API_KEY set in `.env` at repo root

### Running the Server
```bash
make llama-server
```

Server runs on http://localhost:8321

### Testing the Server
```bash
curl http://localhost:8321/v1/models
```

### Running Patterns
```bash
uv run llama-stack-prompt-chaining
```
