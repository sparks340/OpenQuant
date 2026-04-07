"""Audit logging helpers."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from packages.core.core.logging.logger import get_logger


audit_logger = get_logger("openquant.audit")


def emit_audit_event(
    action: str,
    *,
    actor: str,
    resource: str,
    status: str = "SUCCEEDED",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Emit a normalized audit event and return the structured payload."""
    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "action": action,
        "actor": actor,
        "resource": resource,
        "status": status,
        "metadata": metadata or {},
    }
    audit_logger.info("AUDIT_EVENT", extra={"audit": payload})
    return payload
