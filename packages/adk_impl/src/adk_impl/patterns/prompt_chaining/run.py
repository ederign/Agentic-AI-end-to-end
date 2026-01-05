import os

from common.env import load_repo_dotenv

from .chain import run_prompt_chaining


def main() -> None:
    print("Starting prompt chaining (ADK impl)")
    load_repo_dotenv()

    verbose = os.environ.get("VERBOSE", "").lower() in ("1", "true", "yes")
    input_text = "The new laptop model features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."

    result = run_prompt_chaining(input_text, verbose=verbose)

    print("Result:", result)


if __name__ == "__main__":
    main()
