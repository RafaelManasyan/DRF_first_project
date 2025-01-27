from django.urls import path
from rest_framework.routers import SimpleRouter

from web_sky.views import CourseViewSet, LessonListCreate, LessonRetrieveUpdateDestroy

app_name = "web_sky"

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListCreate.as_view(), name="lessons"),
    path("lessons/<int:pk>/", LessonRetrieveUpdateDestroy.as_view(), name="lesson"),
]
urlpatterns += router.urls
