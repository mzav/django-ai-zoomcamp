from django.test import TestCase
from django.utils import timezone

from todos.models import Todo


class TodoModelTests(TestCase):
    def test_str_returns_title(self):
        t = Todo.objects.create(title="Buy milk")
        self.assertEqual(str(t), "Buy milk")

    def test_default_ordering_unresolved_first_then_due_date_then_updated_desc(self):
        now = timezone.now()
        a = Todo.objects.create(title="A", resolved=False, due_date=now)
        b = Todo.objects.create(title="B", resolved=False, due_date=now + timezone.timedelta(hours=1))
        c = Todo.objects.create(title="C", resolved=True, due_date=now - timezone.timedelta(hours=1))

        # Touch B to be updated more recently than A
        b.title = "B2"
        b.save()

        todos = list(Todo.objects.all())

        # Unresolved (False) before resolved (True)
        self.assertEqual([t.resolved for t in todos], [False, False, True])
        # Among unresolved, earlier due_date first; if equal, newer updated first
        self.assertEqual(todos[0].id, a.id)
        self.assertEqual(todos[1].id, b.id)
