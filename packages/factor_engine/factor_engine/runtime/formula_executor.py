"""Formula executor for MVP operators."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal

from packages.factor_engine.factor_engine.models.factor_frame import FactorFrame, FactorPoint
from packages.factor_engine.factor_engine.operators.cross_sectional import rank_by_date
from packages.factor_engine.factor_engine.operators.time_series import delay_by_symbol, ts_mean_by_symbol
from packages.factor_engine.factor_engine.parser.formula_parser import parse_formula
from packages.factor_engine.factor_engine.validators.formula_validator import FormulaValidator


class FormulaExecutor:
    @staticmethod
    def execute(expression: str, market_rows: list[dict]) -> FactorFrame:
        validation = FormulaValidator.validate(expression)
        if not validation.is_valid:
            raise ValueError("; ".join(validation.errors))

        op, field, arg = parse_formula(expression)
        by_symbol: dict[str, list[tuple[date, Decimal]]] = defaultdict(list)
        by_date: dict[date, dict[str, Decimal]] = defaultdict(dict)

        for row in sorted(market_rows, key=lambda x: (x["symbol"], x["trade_date"])):
            symbol = str(row["symbol"]).upper()
            trade_date = row["trade_date"]
            value = Decimal(str(row[field]))
            by_symbol[symbol].append((trade_date, value))
            by_date[trade_date][symbol] = value

        points: list[FactorPoint] = []
        if op == "RANK":
            ranked = rank_by_date(by_date)
            for trade_date, symbol_values in ranked.items():
                for symbol, value in symbol_values.items():
                    points.append(FactorPoint(symbol=symbol, trade_date=trade_date, value=value))
        elif op == "DELAY":
            delayed = delay_by_symbol(by_symbol, arg or 1)
            for symbol, series in delayed.items():
                for trade_date, value in series:
                    if value is not None:
                        points.append(FactorPoint(symbol=symbol, trade_date=trade_date, value=value))
        elif op == "TS_MEAN":
            meaned = ts_mean_by_symbol(by_symbol, arg or 1)
            for symbol, series in meaned.items():
                for trade_date, value in series:
                    points.append(FactorPoint(symbol=symbol, trade_date=trade_date, value=value))
        else:
            raise ValueError(f"Unsupported operator: {op}")

        return FactorFrame(points=points)
