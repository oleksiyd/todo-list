from __future__ import annotations
from flask_wtf import FlaskForm

class BaseForm(FlaskForm):
    """
    Common base class for forms.

    Tracks whether validate() has been called and whether it succeeded,
    so methods like to_model() can enforce correct call order.
    """

    _was_validated: bool = False
    _is_valid: bool = False

    def validate(self, extra_validators=None) -> bool:
        """
        Override the parent validate method to be able to check if
        a form was validated.
        """
        rv = super().validate(extra_validators=extra_validators)
        self._was_validated = True
        self._is_valid = rv
        return rv

    def require_validated(self) -> None:
        """
        Ensure validate()/validate_on_submit() has been called.
        """
        if not getattr(self, "_was_validated", False):
            raise RuntimeError("Call validate()/validate_on_submit() before using this form result.")

    def require_valid(self) -> None:
        """
        Ensure validate()/validate_on_submit() has been called AND succeeded.
        """
        self.require_validated()
        if not getattr(self, "_is_valid", False):
            raise ValueError("Cannot use form results because validation failed.")
