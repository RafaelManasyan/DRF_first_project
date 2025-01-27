from django.db import models


class Course(models.Model):
    """
    Модель курса, содержащая информацию о названии, превью-картинке и описании курса.
    """

    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса (максимум 150 символов).",
    )
    preview_image = models.ImageField(
        upload_to="media/preview_images",
        blank=True,
        null=True,
        verbose_name="Картинка превью",
        help_text="Загрузите картинку для превью курса (необязательно).",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание курса (необязательно).",
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        """
        Строковое представление объекта курса (его название).
        """
        return self.name


class Lesson(models.Model):
    """
    Модель урока, содержащая информацию о названии, превью-картинке, описании, ссылке на урок и связи с курсом.
    """

    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока (максимум 150 символов).",
    )
    preview_image = models.ImageField(
        upload_to="media/preview_images",
        verbose_name="Картинка урока",
        blank=True,
        null=True,
        help_text="Загрузите картинку для урока (необязательно).",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание урока (необязательно).",
    )
    lesson_link = models.CharField(
        verbose_name="Ссылка на урок",
        blank=True,
        null=True,
        help_text="Добавьте ссылку на урок (необязательно).",
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс, к которому относится данный урок.",
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        """
        Строковое представление объекта урока: его название и связанный курс.
        Если курс отсутствует, указывается "Без курса".
        """
        return f"{self.name} ({self.course.name if self.course else 'Без курса'})"
