"""Base factor cleaner."""


def clean_base_factor_rows(rows: list[dict]) -> list[dict]:
    return [
        {
            "factor_id": str(row["factor_id"]).strip(),
            "name": str(row["name"]).strip(),
            "code": str(row["code"]).strip(),
        }
        for row in rows
    ]
