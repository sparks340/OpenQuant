"""Analysis service for Phase F MVP."""

from __future__ import annotations

from collections import defaultdict
from datetime import date

from packages.analysis_engine.analysis_engine.backtest.grouping import assign_groups
from packages.analysis_engine.analysis_engine.backtest.ic import pearson_ic
from packages.analysis_engine.analysis_engine.preprocess.outlier import clip_by_mad
from packages.analysis_engine.analysis_engine.preprocess.standardize import zscore
from packages.analysis_engine.analysis_engine.reports.report_builder import build_report


class AnalysisService:
    """Produce minimal deterministic analysis report from factor + market rows."""

    REQUIRED_FACTOR_KEYS = {"symbol", "trade_date", "factor_value"}
    REQUIRED_MARKET_KEYS = {"symbol", "trade_date", "close"}

    @classmethod
    def run(
        cls,
        factor_rows: list[dict],
        market_rows: list[dict],
        *,
        group_count: int = 5,
    ) -> dict:
        if group_count <= 0:
            raise ValueError("group_count must be positive")
        cls._validate_rows(factor_rows, required_keys=cls.REQUIRED_FACTOR_KEYS, row_name="factor_rows")
        cls._validate_rows(market_rows, required_keys=cls.REQUIRED_MARKET_KEYS, row_name="market_rows")

        market_by_symbol: dict[str, list[tuple[date, float]]] = defaultdict(list)
        for row in market_rows:
            market_by_symbol[str(row["symbol"]).upper()].append((row["trade_date"], float(row["close"])))

        forward_return_map: dict[tuple[str, date], float] = {}
        for symbol, series in market_by_symbol.items():
            sorted_series = sorted(series, key=lambda item: item[0])
            for idx in range(len(sorted_series) - 1):
                trade_date, close_price = sorted_series[idx]
                _, next_close = sorted_series[idx + 1]
                if close_price == 0:
                    continue
                forward_return_map[(symbol, trade_date)] = (next_close / close_price) - 1.0

        cross_section: dict[date, list[tuple[str, float, float]]] = defaultdict(list)
        for row in factor_rows:
            symbol = str(row["symbol"]).upper()
            trade_date = row["trade_date"]
            forward = forward_return_map.get((symbol, trade_date))
            if forward is None:
                continue
            cross_section[trade_date].append((symbol, float(row["factor_value"]), forward))

        ic_by_date: dict[str, float] = {}
        group_return_by_date: dict[str, dict[str, float]] = {}
        top_minus_bottom: list[float] = []

        for trade_date, rows in sorted(cross_section.items(), key=lambda item: item[0]):
            if len(rows) < 2:
                continue

            symbols = [symbol for symbol, _, _ in rows]
            factor_values = [value for _, value, _ in rows]
            returns = [ret for _, _, ret in rows]

            clipped = clip_by_mad(factor_values)
            standardized = zscore(clipped)
            symbol_to_score = dict(zip(symbols, standardized, strict=True))
            groups = assign_groups(symbol_to_score, group_count=group_count)

            factor_for_ic = [symbol_to_score[symbol] for symbol in symbols]
            ic = pearson_ic(factor_for_ic, returns)
            date_key = trade_date.isoformat()
            ic_by_date[date_key] = ic

            grouped_values: dict[int, list[float]] = defaultdict(list)
            for symbol, _, ret in rows:
                grouped_values[groups[symbol]].append(ret)

            per_group: dict[str, float] = {}
            for group_id, group_returns in sorted(grouped_values.items()):
                per_group[str(group_id)] = sum(group_returns) / len(group_returns)
            group_return_by_date[date_key] = per_group

            if per_group:
                min_group = min(grouped_values)
                max_group = max(grouped_values)
                top_minus_bottom.append(per_group[str(max_group)] - per_group[str(min_group)])

        mean_ic = (sum(ic_by_date.values()) / len(ic_by_date)) if ic_by_date else 0.0
        tmb_mean = (sum(top_minus_bottom) / len(top_minus_bottom)) if top_minus_bottom else 0.0

        return build_report(
            ic_by_date=ic_by_date,
            mean_ic=mean_ic,
            group_return_by_date=group_return_by_date,
            top_minus_bottom_mean=tmb_mean,
        )

    @staticmethod
    def _validate_rows(rows: list[dict], *, required_keys: set[str], row_name: str) -> None:
        for index, row in enumerate(rows):
            missing = required_keys.difference(row.keys())
            if missing:
                missing_fields = ",".join(sorted(missing))
                raise ValueError(f"{row_name}[{index}] missing required fields: {missing_fields}")
