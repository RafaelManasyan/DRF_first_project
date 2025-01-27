from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса")
    preview_image = models.ImageField(
        upload_to="media/preview_images",
        blank=True,
        null=True,
        verbose_name="Картинка превью",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока")
    preview_image = models.ImageField(
        upload_to="media/preview_images",
        verbose_name="Картинка урока",
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    lesson_link = models.CharField(verbose_name="Ссылка на урок", blank=True, null=True)
    course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        return f"{self.name} ({self.course.name if self.course else 'Без курса'})"
