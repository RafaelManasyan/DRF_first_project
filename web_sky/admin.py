from django.contrib import admin

from web_sky.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'owner'
