from .base_form import BaseForm
from datetime import datetime, date
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional, Length
from ..models.todo import Todo
import logging

logger = logging.getLogger(__name__)

class IsoDateField(DateField):
    """DateField that also accepts ISO 'YYYY-MM-DD' strings when using obj=/process()."""

    def process_data(self, value):
        if isinstance(value, str) and value:
            value = date.fromisoformat(value)
        return super().process_data(value)

class TodoForm(BaseForm):
    title = StringField(
        "Title",
        validators=[DataRequired(message="Title is required."), Length(max=200)],
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=5000)],
    )
    dueDate = IsoDateField(
        "Due Date",
        format="%Y-%m-%d",
        validators=[Optional()],
    )

    def to_model(self, todo_id: int | None = None) -> Todo:
        """
        Create a Todo model from validated form data.

        Must be called only after validate()/validate_on_submit().
        """
        self.require_valid()

        return Todo(
            id=todo_id or 0,  # service will overwrite if needed
            title=self.title.data.strip(),
            description=self.description.data or None,
            dueDate=self.dueDate.data.isoformat() if self.dueDate.data else None
        )
