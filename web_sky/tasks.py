from celery import shared_task
from django.core.mail import send_mail

from web_sky.models import Subscription, Course


@shared_task()
def send_course_updating_mail(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return

    try:
        subscription = Subscription.objects.get(course=course)
    except Subscription.DoesNotExist:
        return

    subscribers = subscription.user.all()

    send_mail(
        subject=f"Обновление курса: {course.name}",
        message=f"Здравствуйте!\n\nКурс '{course.name}' был обновлен. "
                "Пожалуйста, проверьте изменения.",
        from_email='tmanasyan777@mail.ru',
        recipient_list=[user.email for user in subscribers],
        fail_silently=False,
    )
