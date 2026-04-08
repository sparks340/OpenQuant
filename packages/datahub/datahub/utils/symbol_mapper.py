"""Symbol mapping helpers."""


def normalize_cn_symbol(symbol: str, exchange: str | None = None) -> str:
    clean = symbol.strip().upper()
    if clean.startswith(("SZ", "SH")):
        return clean
    exchange_part = (exchange or "").strip().upper()
    if exchange_part not in {"SZ", "SH"}:
        exchange_part = "SZ" if clean.startswith(("0", "3")) else "SH"
    return f"{exchange_part}{clean}"
