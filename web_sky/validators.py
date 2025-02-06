from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    """Валидатор, который проверяет, что ссылка ведёт только на youtube.com."""
    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()
    if 'youtube.com' not in domain:
        raise ValidationError("Допускаются только ссылки на youtube.com.")
