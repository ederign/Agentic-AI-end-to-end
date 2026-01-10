# ABOUTME: Unified CLI for running prompt chaining with different approaches.
# ABOUTME: Usage: prompt-chaining --approach [raw|langchain|adk]

import argparse
import os

from common.env import load_repo_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run prompt chaining pattern with different approaches"
    )
    parser.add_argument(
        "--approach",
        "-a",
        choices=["raw", "langchain", "adk"],
        default="raw",
        help="Which implementation to use (default: raw)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="The new laptop model features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD.",
        help="Input text to process",
    )
    args = parser.parse_args()

    load_repo_dotenv()
    verbose = args.verbose or os.environ.get("VERBOSE", "").lower() in (
        "1",
        "true",
        "yes",
    )

    print(f"Running prompt chaining with approach: {args.approach}")
    if verbose:
        print("Verbose mode enabled")
    print()

    if args.approach == "raw":
        from .raw import run_prompt_chaining
    elif args.approach == "langchain":
        from .langchain import run_prompt_chaining
    elif args.approach == "adk":
        from .adk import run_prompt_chaining
    else:
        raise ValueError(f"Unknown approach: {args.approach}")

    result = run_prompt_chaining(args.input, verbose=verbose)
    print("Result:", result)


if __name__ == "__main__":
    main()
