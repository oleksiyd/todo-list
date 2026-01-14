from flask import Flask
import os
import logging
from .services.todo_service import TodoService
from .controllers.todo_controller import todo_bp
from .filters import register_filters
from .bootstrap import AppInitializer
from app.constants import KEY_DATA_FILE, KEY_SECRET_KEY, KEY_LOG_LEVEL

def create_app(config: dict | None = None) -> Flask:
    # Initialize the Flask application
    app = Flask(__name__, template_folder="templates")
    # Assign global variables from environment variables
    app.config.from_mapping(
        # Data file location
        DATA_FILE=os.getenv(KEY_DATA_FILE, "data/todos.json"),
        # Secret key for signing session cookies, generating CSRF tokens, etc
        SECRET_KEY=os.getenv(KEY_SECRET_KEY, "dev"),
        # Enable CSRF protection
        WTF_CSRF_ENABLED=True,
    )
    # Add additional configuration if provided
    if config:
        app.config.update(config)

    # Read log level from environment (default: DEBUG)
    log_level_name = os.getenv(KEY_LOG_LEVEL, "DEBUG").upper()
    log_level = getattr(logging, log_level_name, logging.DEBUG)
    app.logger.setLevel(log_level)

    # Register Jinja template filters
    register_filters(app)

    # App wiring (services + routes)
    AppInitializer.init_app(app)

    return app
