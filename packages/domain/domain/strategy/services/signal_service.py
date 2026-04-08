"""Strategy signal domain helpers."""

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.domain.domain.strategy.entities.signal import Signal


class SignalService:
    """Signal ranking helpers used by strategy flows."""

    @staticmethod
    def rank_signals(signals: list[Signal], top_n: int) -> list[Signal]:
        if top_n <= 0:
            raise InvariantViolationError("top_n must be positive")

        dedup: dict[str, Signal] = {}
        for signal in signals:
            existing = dedup.get(signal.symbol)
            if existing is None or signal.score > existing.score:
                dedup[signal.symbol] = signal

        return sorted(dedup.values(), key=lambda item: item.score, reverse=True)[:top_n]
