from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from web_sky.models import Course, Lesson
from web_sky.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """
    ViewSet для модели Course.
    Обеспечивает полный набор операций CRUD (создание, чтение, обновление, удаление) для курсов.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreate(ListCreateAPIView):
    """
    Представление для получения списка уроков (GET) и создания нового урока (POST).
    - GET: Возвращает список всех уроков.
    - POST: Создаёт новый урок с указанными данными.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    Представление для работы с конкретным уроком.
    - GET: Возвращает детали урока по его ID.
    - PUT/PATCH: Обновляет данные урока.
    - DELETE: Удаляет урок.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
