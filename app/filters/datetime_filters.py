from datetime import datetime

def format_utc(value: str) -> str:
    """
    Format an ISO-8601 UTC datetime string into a user-friendly format.
    """
    if not value:
        return ""

    dt = datetime.fromisoformat(value)
    return dt.strftime("%B %d, %Y at %H:%M UTC")
