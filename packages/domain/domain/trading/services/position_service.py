"""Position domain service."""

from decimal import Decimal

from packages.core.core.enums.trading import OrderSide
from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.trading.entities.position import Position
from packages.domain.domain.trading.entities.trade import Trade


class PositionService:
    """Apply trade fills into positions."""

    @staticmethod
    def apply_trade(position: Position, trade: Trade) -> Position:
        if trade.side == OrderSide.BUY:
            new_quantity = position.quantity + trade.quantity
            new_average_price = (
                (position.average_price * position.quantity) + (trade.price * trade.quantity)
            ) / new_quantity
            return Position(symbol=position.symbol, quantity=new_quantity, average_price=new_average_price)

        # SELL
        if trade.quantity > position.quantity:
            raise InvariantViolationError("sell quantity cannot exceed position quantity")
        new_quantity = position.quantity - trade.quantity
        new_average_price = position.average_price if new_quantity > Decimal("0") else Decimal("0")
        return Position(symbol=position.symbol, quantity=new_quantity, average_price=new_average_price)
