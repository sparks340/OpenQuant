"""Risk service for Phase J MVP."""

from __future__ import annotations

from decimal import Decimal

from packages.portfolio_engine.portfolio_engine.builders.order_intent_builder import OrderIntent
from packages.risk_engine.risk_engine.models.risk_context import RiskContext
from packages.risk_engine.risk_engine.models.risk_result import OrderRiskDecision
from packages.risk_engine.risk_engine.rules.blacklist import check_blacklist
from packages.risk_engine.risk_engine.rules.cash_reserve import check_cash_reserve
from packages.risk_engine.risk_engine.rules.max_position_weight import check_max_position_weight


class RiskService:
    def __init__(
        self,
        *,
        max_position_weight: Decimal = Decimal("0.2"),
        min_cash_reserve: Decimal = Decimal("0.05"),
    ) -> None:
        self.max_position_weight = max_position_weight
        self.min_cash_reserve = min_cash_reserve

    def evaluate_orders(self, *, intents: list[OrderIntent], context: RiskContext) -> list[OrderRiskDecision]:
        decisions: list[OrderRiskDecision] = []
        for intent in intents:
            reasons: list[str] = []

            blacklist_hit = check_blacklist(intent, context)
            if blacklist_hit:
                reasons.append(blacklist_hit)

            cash_hit = check_cash_reserve(intent, context, self.min_cash_reserve)
            if cash_hit:
                reasons.append(cash_hit)

            weight_hit = check_max_position_weight(intent, context, self.max_position_weight)
            if weight_hit:
                reasons.append(weight_hit)

            approved = len(reasons) == 0
            decisions.append(
                OrderRiskDecision(
                    intent=intent,
                    approved=approved,
                    reasons=reasons if reasons else ["approved"],
                )
            )
        return decisions
