"""Build target positions from target weights."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from packages.domain.domain.strategy.entities.target_position import TargetPosition


class TargetBuilder:
    @staticmethod
    def build(target_weights: dict[str, Decimal]) -> list[TargetPosition]:
        return [
            TargetPosition(
                symbol=symbol,
                target_weight=weight.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP),
            )
            for symbol, weight in sorted(target_weights.items())
        ]
