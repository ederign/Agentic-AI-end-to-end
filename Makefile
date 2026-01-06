.PHONY: llama-server

llama-server:
	set -a && source .env && set +a && uv run --with llama-stack llama stack run llamastack-run.yaml
