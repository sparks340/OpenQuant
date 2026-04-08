"""Backtest job stub for phase H."""


def run_backtest_job(payload: dict) -> dict:
    if payload.get("should_fail"):
        raise ValueError("backtest job failed by payload flag")
    return {"result": "backtest_done", "payload": payload}
