from django.contrib import admin
from .models import Task
# Register your models here.

# admin.site.register(Task)
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'created_at', 'updated_at')