from django.test import SimpleTestCase

from todos.forms import TodoForm


class TodoFormTests(SimpleTestCase):
    def test_due_date_widget_is_datetime_local(self):
        form = TodoForm()
        self.assertEqual(form.fields["due_date"].widget.input_type, "datetime-local")

    def test_title_is_required(self):
        form = TodoForm(data={"title": "", "description": "", "resolved": False})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_valid_data_succeeds(self):
        form = TodoForm(data={"title": "Task", "description": "", "resolved": False})
        self.assertTrue(form.is_valid())
