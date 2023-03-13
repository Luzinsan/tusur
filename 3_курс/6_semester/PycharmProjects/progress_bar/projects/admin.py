from django.contrib import admin

from .models import Project
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date', 'project')
    list_display_links = ('title', 'description')
    search_fields = ('title', 'description', 'project')


admin.site.register(Project)
admin.site.register(Task, TaskAdmin)

