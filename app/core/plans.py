FREE_DAILY_LIMIT = 20


def get_daily_limit(plan: str) -> int:
    if plan == "PAID":
        return 10000
    return FREE_DAILY_LIMIT
