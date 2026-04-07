"""LLM service entrypoint.

The dedicated service boundary keeps model integration isolated from trading
and research execution, which reduces coupling and deployment risk later.
"""


def main() -> None:
    """Start the LLM service placeholder process."""
    print("llm service bootstrap completed")


if __name__ == "__main__":
    main()

