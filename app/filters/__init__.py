from flask import Flask
from .datetime_filters import format_utc

def register_filters(app: Flask) -> None:
    """
    Register all Jinja template filters.
    """
    app.add_template_filter(format_utc, name="format_utc")
