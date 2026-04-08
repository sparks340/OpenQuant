"""Portfolio service for Phase I MVP."""

from __future__ import annotations

from decimal import Decimal

from packages.domain.domain.strategy.entities.target_position import TargetPosition
from packages.portfolio_engine.portfolio_engine.allocators.score_weight import ScoreWeightAllocator
from packages.portfolio_engine.portfolio_engine.builders.order_intent_builder import OrderIntent, OrderIntentBuilder
from packages.portfolio_engine.portfolio_engine.builders.target_builder import TargetBuilder


class PortfolioService:
    def __init__(self) -> None:
        self._allocator = ScoreWeightAllocator()

    def build_target_positions(
        self,
        *,
        scores: dict[str, Decimal],
        top_n: int,
        max_single_weight: Decimal,
    ) -> list[TargetPosition]:
        target_weights = self._allocator.allocate(
            scores=scores,
            top_n=top_n,
            max_single_weight=max_single_weight,
        )
        return TargetBuilder.build(target_weights)

    def build_order_intents(
        self,
        *,
        account_id: str,
        total_equity: Decimal,
        targets: list[TargetPosition],
        latest_prices: dict[str, Decimal],
        current_positions: dict[str, Decimal],
    ) -> list[OrderIntent]:
        target_weights = {target.symbol: target.target_weight for target in targets}
        return OrderIntentBuilder.build(
            account_id=account_id,
            total_equity=total_equity,
            target_weights=target_weights,
            latest_prices={symbol.upper(): price for symbol, price in latest_prices.items()},
            current_positions={symbol.upper(): qty for symbol, qty in current_positions.items()},
        )
