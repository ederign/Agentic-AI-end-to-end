.PHONY: llama-server

llama-server:
	set -a && source .env && set +a && uv run --with 'llama-stack @ git+https://github.com/meta-llama/llama-stack.git@v0.4.0rc2' --with faiss-cpu llama stack run llamastack-run.yaml
