from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "due_date", "resolved", "updated_at")
    list_filter = ("resolved",)
    search_fields = ("title", "description")
    ordering = ("resolved", "due_date")
