import os

from common.env import load_repo_dotenv


def main() -> None:
    print("Starting prompt chaining (LlamaStack impl)")
    load_repo_dotenv()

    verbose = os.environ.get("VERBOSE", "").lower() in ("1", "true", "yes")
    if verbose:
        print("Verbose mode enabled")

    print("Hello World! - Plumbing works, now implement chain.py")


if __name__ == "__main__":
    main()
