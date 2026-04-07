"""Trading-domain enums shared across packages."""

from enum import StrEnum


class OrderSide(StrEnum):
    """Supported order directions."""

    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(StrEnum):
    """Canonical order lifecycle."""

    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
