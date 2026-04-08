"""Score-based target weight allocator."""

from __future__ import annotations

from decimal import Decimal


class ScoreWeightAllocator:
    def allocate(
        self,
        *,
        scores: dict[str, Decimal],
        top_n: int,
        max_single_weight: Decimal,
    ) -> dict[str, Decimal]:
        if top_n <= 0:
            raise ValueError("top_n must be positive")
        if max_single_weight <= Decimal("0") or max_single_weight > Decimal("1"):
            raise ValueError("max_single_weight must be in (0, 1]")

        ranked = sorted(
            ((symbol.upper(), score) for symbol, score in scores.items() if score > Decimal("0")),
            key=lambda item: (-item[1], item[0]),
        )[:top_n]
        if not ranked:
            return {}

        total = sum((score for _, score in ranked), start=Decimal("0"))
        raw = {symbol: (score / total) for symbol, score in ranked}
        return self._apply_cap(raw, max_single_weight)

    @staticmethod
    def _apply_cap(raw_weights: dict[str, Decimal], max_single_weight: Decimal) -> dict[str, Decimal]:
        remaining = dict(raw_weights)
        capped: dict[str, Decimal] = {}
        budget = Decimal("1")

        while remaining and budget > Decimal("0"):
            remaining_sum = sum(remaining.values(), start=Decimal("0"))
            if remaining_sum <= Decimal("0"):
                break

            breached: list[str] = []
            for symbol, weight in remaining.items():
                proposed = budget * (weight / remaining_sum)
                if proposed > max_single_weight:
                    capped[symbol] = max_single_weight
                    budget -= max_single_weight
                    breached.append(symbol)

            if not breached:
                for symbol, weight in remaining.items():
                    capped[symbol] = budget * (weight / remaining_sum)
                break

            for symbol in breached:
                remaining.pop(symbol, None)

        return capped
