"""Application orchestration services for api_service."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from itertools import count

from packages.analysis_engine.analysis_engine.services.analysis_service import AnalysisService
from packages.factor_engine.factor_engine.runtime.formula_executor import FormulaExecutor


class InMemoryOrchestrationStore:
    def __init__(self) -> None:
        self._factor_seq = count(start=1)
        self._run_seq = count(start=1)
        self._report_seq = count(start=1)
        self.factors: dict[str, dict] = {}
        self.runs: dict[str, dict] = {}
        self.reports: dict[str, dict] = {}

    def create_factor(self, *, name: str, expression: str, description: str) -> dict:
        factor_id = f"FAC-{next(self._factor_seq):04d}"
        factor = {
            "factor_id": factor_id,
            "name": name,
            "expression": expression,
            "description": description,
        }
        self.factors[factor_id] = factor
        return factor

    def run_factor(self, *, factor_id: str, expression: str, market_rows: list[dict], group_count: int) -> dict:
        factor_frame = FormulaExecutor.execute(expression, market_rows)
        factor_rows = [
            {
                "symbol": point.symbol,
                "trade_date": point.trade_date,
                "factor_value": point.value,
            }
            for point in factor_frame.points
        ]

        report = AnalysisService.run(factor_rows, market_rows, group_count=group_count)

        report_id = f"RPT-{next(self._report_seq):04d}"
        run_id = f"RUN-{next(self._run_seq):04d}"
        self.reports[report_id] = report
        run = {
            "run_id": run_id,
            "factor_id": factor_id,
            "report_id": report_id,
            "status": "SUCCEEDED",
        }
        self.runs[run_id] = run
        return run

    def get_report(self, report_id: str) -> dict | None:
        return self.reports.get(report_id)

    def get_account(self, account_id: str) -> dict:
        return {
            "account_id": account_id,
            "cash": Decimal("1000000"),
            "market_value": Decimal("0"),
        }

    def get_positions(self, account_id: str) -> list[dict]:
        _ = account_id
        return []

    def get_orders(self, account_id: str) -> list[dict]:
        _ = account_id
        return []


def normalize_market_rows(rows: list[dict]) -> list[dict]:
    normalized: list[dict] = []
    for row in rows:
        normalized.append(
            {
                "symbol": str(row["symbol"]).upper(),
                "trade_date": row["trade_date"] if isinstance(row["trade_date"], date) else date.fromisoformat(str(row["trade_date"])),
                "close": Decimal(str(row["close"])),
            }
        )
    return normalized
