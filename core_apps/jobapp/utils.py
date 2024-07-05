from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError


def get_all_form_errors(form):
    error_messages = []

    for field, errors in form.errors.as_data().items():
        for error in errors:
            if isinstance(error, ErrorList):
                for e in error:
                    error_messages.append(str(e))
            elif isinstance(error, ValidationError):
                for e in error:
                    error_messages.append(str(e))
            else:
                error_messages.append(str(error))

    return ",".join(error_messages) if error_messages else None