"""Research worker entrypoint.

In later phases this worker will consume factor calculation and analysis tasks.
For now we keep a lightweight placeholder so the service boundary is explicit
from the beginning of the rebuild.
"""


def main() -> None:
    """Start the research worker placeholder process."""
    print("research worker bootstrap completed")


if __name__ == "__main__":
    main()

