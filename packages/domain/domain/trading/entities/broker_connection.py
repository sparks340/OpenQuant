"""Broker connection entity."""

from enum import StrEnum

from packages.core.core.exceptions.domain import InvariantViolationError
from packages.core.core.models.base import CoreModel


class BrokerConnectionStatus(StrEnum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    ERROR = "ERROR"


_VALID_TRANSITIONS: dict[BrokerConnectionStatus, set[BrokerConnectionStatus]] = {
    BrokerConnectionStatus.DISCONNECTED: {BrokerConnectionStatus.CONNECTED, BrokerConnectionStatus.ERROR},
    BrokerConnectionStatus.CONNECTED: {BrokerConnectionStatus.DISCONNECTED, BrokerConnectionStatus.ERROR},
    BrokerConnectionStatus.ERROR: {BrokerConnectionStatus.DISCONNECTED},
}


class BrokerConnection(CoreModel):
    broker_id: str
    account_id: str
    status: BrokerConnectionStatus = BrokerConnectionStatus.DISCONNECTED

    def transition_to(self, target: BrokerConnectionStatus) -> None:
        if target not in _VALID_TRANSITIONS[self.status]:
            raise InvariantViolationError(f"Invalid broker connection transition: {self.status} -> {target}")
        self.status = target
