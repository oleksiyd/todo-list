from flask import Flask
from .services.todo_service import TodoService
from .controllers.todo_controller import todo_bp
from app.constants import KEY_DATA_FILE


class AppInitializer:
    """
    Wires application services and blueprints.
    """

    @staticmethod
    def init_app(app: Flask) -> None:
        # Initialize services
        app.todo_service = TodoService(app.config[KEY_DATA_FILE])

        # Register blueprints
        app.register_blueprint(todo_bp)
