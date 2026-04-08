"""Schemas for analysis APIs."""

from __future__ import annotations

from pydantic import BaseModel


class ReportQueryData(BaseModel):
    report_id: str
    report: dict
