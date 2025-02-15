# Generated by Django 5.1.5 on 2025-01-27 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web_sky", "0002_alter_course_description_alter_course_preview_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="web_sky.course",
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="lesson_link",
            field=models.CharField(
                blank=True, null=True, verbose_name="Ссылка на урок"
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="preview_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="media/preview_images",
                verbose_name="Картинка урока",
            ),
        ),
    ]
