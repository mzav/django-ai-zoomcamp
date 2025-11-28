from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from todos.models import Todo


class TodoViewsTests(TestCase):
    def setUp(self):
        self.list_url = reverse("todos:index")
        self.create_url = reverse("todos:create")

    def test_index_lists_todos_and_now_in_context(self):
        t1 = Todo.objects.create(title="Buy milk")
        t2 = Todo.objects.create(title="Read book")
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, t1.title)
        self.assertContains(resp, t2.title)
        self.assertIn("now", resp.context)

    def test_index_search_filters_by_title_and_description(self):
        Todo.objects.create(title="Alpha", description="x")
        Todo.objects.create(title="Beta", description="contains needle")
        resp = self.client.get(self.list_url, {"q": "needle"})
        self.assertContains(resp, "Beta")
        self.assertNotContains(resp, "Alpha")

    def test_overdue_badge_shows_only_when_unresolved_and_past_due(self):
        past = timezone.now() - timezone.timedelta(days=1)
        future = timezone.now() + timezone.timedelta(days=1)
        overdue = Todo.objects.create(title="Past", due_date=past, resolved=False)
        not_overdue = Todo.objects.create(title="Future", due_date=future, resolved=False)
        resolved_past = Todo.objects.create(title="Resolved Past", due_date=past, resolved=True)

        resp = self.client.get(self.list_url)
        self.assertContains(resp, "Overdue")  # at least for one item
        # Ensure resolved past-due doesn't show Overdue near its title
        self.assertContains(resp, resolved_past.title)
        # Rendered block shouldn't mark resolved past-due as overdue; we can ensure only one occurrence
        self.assertEqual(resp.content.decode("utf-8").count("Overdue"), 1)

    def test_resolved_badge_and_toggle_button_style(self):
        unresolved = Todo.objects.create(title="U", resolved=False)
        resolved = Todo.objects.create(title="R", resolved=True)
        resp = self.client.get(self.list_url)
        # Resolved badge visible for resolved only
        self.assertContains(resp, "Resolved")
        # Toggle button classes per yesno filter
        html = resp.content.decode("utf-8")
        self.assertIn("btn-outline-success", html)  # for unresolved items
        self.assertIn("btn-outline-warning", html)  # for resolved items

    def test_create_get_and_post(self):
        # GET
        resp = self.client.get(self.create_url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Create TODO")

        # POST invalid (missing title)
        resp = self.client.post(self.create_url, {"title": "", "description": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "This field is required", html=False)

        # POST valid
        resp = self.client.post(self.create_url, {"title": "New task", "description": "desc", "resolved": False})
        self.assertRedirects(resp, self.list_url)
        self.assertTrue(Todo.objects.filter(title="New task").exists())

    def test_edit_get_and_post(self):
        t = Todo.objects.create(title="Edit me", description="old")
        url = reverse("todos:edit", args=[t.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Edit TODO")

        resp = self.client.post(url, {"title": "Edited", "description": "new", "resolved": True})
        self.assertRedirects(resp, self.list_url)
        t.refresh_from_db()
        self.assertEqual(t.title, "Edited")
        self.assertTrue(t.resolved)

    def test_delete_get_and_post(self):
        t = Todo.objects.create(title="Delete me")
        url = reverse("todos:delete", args=[t.id])
        # GET confirm page
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Delete TODO")
        # POST delete
        resp = self.client.post(url)
        self.assertRedirects(resp, self.list_url)
        self.assertFalse(Todo.objects.filter(id=t.id).exists())

    def test_toggle_resolved_and_redirects_respecting_next(self):
        t = Todo.objects.create(title="Toggle", resolved=False)
        url = reverse("todos:toggle", args=[t.id])
        # With next parameter
        next_url = self.list_url + "?q=test"
        resp = self.client.get(f"{url}?next={next_url}")
        self.assertRedirects(resp, next_url)
        t.refresh_from_db()
        self.assertTrue(t.resolved)
        # Without next, redirect to index
        resp = self.client.get(url)
        self.assertRedirects(resp, self.list_url)
