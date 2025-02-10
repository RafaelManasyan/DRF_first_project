from django.urls import path
from rest_framework.routers import SimpleRouter

from web_sky.views import (CourseViewSet, LessonCreate, LessonDestroy,
                           LessonList, LessonRetrieveUpdate,
                           SubscriptionAPIView)

app_name = "web_sky"

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonList.as_view(), name="lessons"),
    path("lessons/create/", LessonCreate.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/", LessonRetrieveUpdate.as_view(), name="lesson"),
    path("lessons/<int:pk>/delete/", LessonDestroy.as_view(), name='lesson-delete'),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription")
]
urlpatterns += router.urls
