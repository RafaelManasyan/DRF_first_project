from django.contrib import admin

from web_sky.models import Course, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'owner'


@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    list_display = 'id', 'course', 'created_at'
