from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task()
def deactivate_inactive_users():
    """ Деактивирует пользователей, которые не входили в систему более 30 дней."""
    time_gap = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True, last_login__lt=time_gap)
    inactive_users.update(is_active=False)
