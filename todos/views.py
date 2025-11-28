from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .models import Todo
from .forms import TodoForm


def index(request):
    query = request.GET.get("q", "").strip()
    todos = Todo.objects.all()
    if query:
        todos = todos.filter(title__icontains=query) | todos.filter(description__icontains=query)
    context = {
        "todos": todos,
        "now": timezone.now(),
        "query": query,
    }
    return render(request, "todos/list.html", context)


def create(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todos:index")
    else:
        form = TodoForm()
    return render(request, "todos/form.html", {"form": form, "action": "Create"})


def edit(request, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("todos:index")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todos/form.html", {"form": form, "action": "Edit"})


def delete(request, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        todo.delete()
        return redirect("todos:index")
    return render(request, "todos/confirm_delete.html", {"todo": todo})


def toggle_resolved(request, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    todo.resolved = not todo.resolved
    todo.save(update_fields=["resolved", "updated_at"])
    return redirect(request.GET.get("next") or reverse("todos:index"))
