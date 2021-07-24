from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_pk(value):
    if ' ' in value:
        raise ValidationError(
            _('space is not allowed in %(value)s'),
            params={'value': value},
        )