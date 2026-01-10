# Common

Shared utilities used across all pattern implementations.

## Usage

```python
from common.env import load_repo_dotenv

# Loads .env from repository root
load_repo_dotenv()
```

## What It Provides

| Function | Purpose |
|----------|---------|
| `load_repo_dotenv()` | Loads environment variables from repo root `.env` file |

## Why It Exists

Each package in the workspace needs access to API keys (e.g., `OPENAI_API_KEY`). Instead of duplicating `.env` loading logic, all packages depend on `common` and call `load_repo_dotenv()`.
