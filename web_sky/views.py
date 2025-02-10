from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModers, IsOwner
from web_sky.models import Course, Lesson, Subscription
from web_sky.paginators import PagePagination
from web_sky.serializers import CourseSerializer, LessonSerializer
from web_sky.tasks import send_course_updating_mail


class CourseViewSet(ModelViewSet):
    """
    ViewSet для модели Course.
    Обеспечивает полный набор операций CRUD (создание, чтение, обновление, удаление) для курсов.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = PagePagination

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        course_id = kwargs.get('pk')

        if course_id:
            send_course_updating_mail.delay(course_id)
        return response

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
    pagination_class = PagePagination


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


class SubscriptionAPIView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({"message": "Не указан course_id."}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(course=course)

        if subscription.user.filter(pk=user.pk).exists():
            subscription.user.remove(user)
            message = "Подписка удалена"
        else:
            subscription.user.add(user)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)

