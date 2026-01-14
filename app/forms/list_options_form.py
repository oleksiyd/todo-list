from .base_form import BaseForm
from wtforms import SelectField
from wtforms.validators import AnyOf, Optional
from ..models.list_options import ListOptions, KEY_ALL, KEY_PENDING, KEY_COMPLETED, KEY_CREATED_AT, KEY_DUE_DATE, KEY_TITLE, KEY_ASC, KEY_DESC

class ListOptionsForm(BaseForm):
    """GET form for filtering/sorting on the index page.

    CSRF is disabled because this form uses GET and does not mutate state.
    """

    class Meta:
        csrf = False

    status = SelectField(
        "Status",
        choices=[
            (KEY_ALL, "All"),
            (KEY_PENDING, "Pending"),
            (KEY_COMPLETED, "Completed"),
        ],
        default=KEY_ALL,
        validators=[Optional(), AnyOf([KEY_ALL, KEY_PENDING, KEY_COMPLETED])],
    )

    sort = SelectField(
        "Sort by",
        choices=[
            (KEY_CREATED_AT, "Created"),
            (KEY_DUE_DATE, "Due date"),
            (KEY_TITLE, "Title"),
        ],
        default=KEY_CREATED_AT,
        validators=[Optional(), AnyOf([KEY_CREATED_AT, KEY_DUE_DATE, KEY_TITLE])],
    )

    order = SelectField(
        "Order",
        choices=[
            (KEY_ASC, "Ascending"),
            (KEY_DESC, "Descending"),
        ],
        default=KEY_DESC,
        validators=[Optional(), AnyOf([KEY_ASC, KEY_DESC])],
    )

    def set_defaults(self):
        """ Sets the form fields to default values """
        self.status=KEY_ALL
        self.sort=KEY_CREATED_AT
        self.order=KEY_DESC

    def to_model(self) -> ListOptions:
        """
        Create a ListOptions model from validated form data.

        Must be called only after validate()/validate_on_submit().
        """
        self.require_valid()

        return ListOptions(
            status=self.status.data.strip().lower(),
            sort=self.sort.data.strip().lower(),
            order=self.order.data.strip().lower(),
        )
