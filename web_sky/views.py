from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, RetrieveUpdateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModers, IsOwner
from web_sky.models import Course, Lesson
from web_sky.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """
    ViewSet для модели Course.
    Обеспечивает полный набор операций CRUD (создание, чтение, обновление, удаление) для курсов.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', ]:
            self.permission_classes = (~IsModers,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModers | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner, )
        return super().get_permissions()


class LessonList(ListAPIView):
    """
    Представление для получения списка уроков (GET) и создания нового урока (POST).
    - GET: Возвращает список всех уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModers | IsAuthenticated, )


class LessonCreate(CreateAPIView):
    """
    Представление для получения списка уроков (GET) и создания нового урока (POST).
    - POST: Создаёт новый урок с указанными данными.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModers,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveUpdate(RetrieveUpdateAPIView):
    """
    Представление для работы с конкретным уроком.
    - GET: Возвращает детали урока по его ID.
    - PUT/PATCH: Обновляет данные урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModers | IsOwner,)


class LessonDestroy(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner,)
