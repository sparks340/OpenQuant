"""Minimal SDK entrypoint.

The SDK will let notebooks or standalone strategy scripts call platform
capabilities without duplicating request logic.
"""


class OpenQuantClient:
    """Tiny placeholder client for phase 1 scaffolding."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
