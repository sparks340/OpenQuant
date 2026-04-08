"""Schemas for factor APIs."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class FactorCreateRequest(BaseModel):
    name: str
    expression: str
    description: str = ""


class FactorCreateData(BaseModel):
    factor_id: str
    name: str
    expression: str


class MarketRowPayload(BaseModel):
    symbol: str
    trade_date: date
    close: Decimal


class FactorRunRequest(BaseModel):
    factor_id: str
    expression: str
    market_rows: list[MarketRowPayload]
    group_count: int = Field(default=5, ge=1)


class FactorRunData(BaseModel):
    run_id: str
    factor_id: str
    report_id: str
    status: str
