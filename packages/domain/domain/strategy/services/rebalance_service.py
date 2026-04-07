"""Rebalance domain service."""

from __future__ import annotations

from decimal import Decimal

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.strategy.entities.rebalance_plan import RebalancePlan
from packages.domain.domain.strategy.entities.signal import Signal


class RebalanceService:
    """Convert signals into a bounded target-allocation plan."""

    def build_plan(
        self,
        *,
        plan_id: str,
        strategy_version_id: str,
        signals: list[Signal],
        top_n: int = 10,
        max_single_weight: Decimal = Decimal("0.2"),
    ) -> RebalancePlan:
        if top_n <= 0:
            raise InvariantViolationError("top_n must be positive")
        if max_single_weight <= Decimal("0") or max_single_weight > Decimal("1"):
            raise InvariantViolationError("max_single_weight must be in (0, 1]")

        positive_signals = [sig for sig in signals if sig.score > Decimal("0")]
        ranked = sorted(positive_signals, key=lambda item: item.score, reverse=True)[:top_n]
        if not ranked:
            raise InvariantViolationError("No positive signals available for rebalance")

        total_score = sum((sig.score for sig in ranked), start=Decimal("0"))
        raw_targets = {sig.symbol: (sig.score / total_score) for sig in ranked}
        normalized_targets = self._apply_single_name_cap(raw_targets, max_single_weight)

        return RebalancePlan(
            plan_id=plan_id,
            strategy_version_id=strategy_version_id,
            targets=normalized_targets,
        )

    @staticmethod
    def _apply_single_name_cap(
        raw_targets: dict[str, Decimal], max_single_weight: Decimal
    ) -> dict[str, Decimal]:
        remaining = dict(raw_targets)
        final_targets: dict[str, Decimal] = {}
        budget = Decimal("1")

        while remaining and budget > Decimal("0"):
            remaining_sum = sum(remaining.values(), start=Decimal("0"))
            if remaining_sum <= Decimal("0"):
                break

            breached: list[str] = []
            for symbol, raw_weight in remaining.items():
                proposed = budget * (raw_weight / remaining_sum)
                if proposed > max_single_weight:
                    final_targets[symbol] = max_single_weight
                    budget -= max_single_weight
                    breached.append(symbol)

            if not breached:
                for symbol, raw_weight in remaining.items():
                    final_targets[symbol] = budget * (raw_weight / remaining_sum)
                budget = Decimal("0")
                break

            for symbol in breached:
                remaining.pop(symbol, None)

        return final_targets
