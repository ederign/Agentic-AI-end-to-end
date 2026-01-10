.PHONY: llama-server prompt-chaining-raw prompt-chaining-langchain prompt-chaining-adk prompt-chaining-all lint typecheck check setup-hooks

# LlamaStack server (required for raw and langchain approaches)
llama-server:
	set -a && source .env && set +a && uv run --with 'llama-stack @ git+https://github.com/meta-llama/llama-stack.git@v0.4.0rc2' --with faiss-cpu llama stack run config/llamastack-run.yaml

# Prompt chaining pattern - individual approaches
prompt-chaining-raw:
	uv run --package patterns prompt-chaining --approach raw

prompt-chaining-langchain:
	uv run --package patterns prompt-chaining --approach langchain

prompt-chaining-adk:
	uv run --package patterns prompt-chaining --approach adk

# Run all three approaches for comparison
prompt-chaining-all:
	@echo "=== Raw (LlamaStack Responses API) ===" && \
	uv run --package patterns prompt-chaining --approach raw && \
	echo "" && \
	echo "=== LangChain + LlamaStack ===" && \
	uv run --package patterns prompt-chaining --approach langchain && \
	echo "" && \
	echo "=== ADK (LiteLLM) ===" && \
	uv run --package patterns prompt-chaining --approach adk

# Code quality checks (fail build if issues found)
lint:
	uv run ruff check .

typecheck:
	uv run pyright

check: lint typecheck
	@echo "All checks passed!"

# Setup git hooks (run once after cloning)
setup-hooks:
	git config core.hooksPath .githooks
	@echo "Git hooks configured!"
