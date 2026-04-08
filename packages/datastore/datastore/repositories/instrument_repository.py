"""Instrument repository for standardized symbol universe."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Instrument:
    symbol: str
    name: str


class InstrumentRepository(ABC):
    @abstractmethod
    def save(self, instrument: Instrument) -> Instrument: ...

    @abstractmethod
    def list_all(self) -> list[Instrument]: ...


class InMemoryInstrumentRepository(InstrumentRepository):
    def __init__(self) -> None:
        self._instruments: dict[str, Instrument] = {}

    def save(self, instrument: Instrument) -> Instrument:
        self._instruments[instrument.symbol] = instrument
        return instrument

    def list_all(self) -> list[Instrument]:
        return list(self._instruments.values())
