from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from web_sky.models import Course, Lesson
from web_sky.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    lesson_link = serializers.CharField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов с подсчётом количества уроков"""

    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    lesson_total = SerializerMethodField()

    def get_lesson_total(self, obj):
        """Возвращает количество уроков в данном курсе"""
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = "__all__"
