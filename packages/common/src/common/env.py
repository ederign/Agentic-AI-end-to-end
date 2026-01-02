from __future__ import annotations

from dotenv import load_dotenv
from pathlib import Path


def load_repo_dotenv(filename: str = ".env") -> None:
    # Resolve repo root: packages/common/src/common/env.py -> repo root
    repo_root = Path(__file__).resolve().parents[4]
    load_dotenv(repo_root / filename, override=False)
