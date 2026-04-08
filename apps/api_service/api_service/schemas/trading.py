"""Schemas for trading query APIs."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class AccountData(BaseModel):
    account_id: str
    cash: Decimal
    market_value: Decimal


class AccountQueryData(BaseModel):
    account: AccountData


class PositionData(BaseModel):
    symbol: str
    quantity: Decimal


class PositionsQueryData(BaseModel):
    account_id: str
    positions: list[PositionData]


class OrderData(BaseModel):
    order_id: str
    symbol: str
    side: str
    quantity: Decimal
    status: str


class OrdersQueryData(BaseModel):
    account_id: str
    orders: list[OrderData]
