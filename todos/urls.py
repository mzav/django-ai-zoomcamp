from django.urls import path
from . import views


app_name = "todos"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/toggle/", views.toggle_resolved, name="toggle"),
]
