from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from .models import Task, Category
from .views import home, delete_task
from .forms import TaskForm


class HomeViewTestCase(TestCase):
    """Test cases for the home view."""

    def setUp(self):
        """Set up test data before each test."""
        self.client = Client()
        # Create test categories
        self.category_work = Category.objects.create(name="Work")

        # Create test tasks - to-do tasks
        self.todo_task1 = Task.objects.create(
            title="Task 1 - Todo",
            due_date=date.today() + timedelta(days=1),
            is_completed=False,
            category=self.category_work
        )

        # Create test tasks - done tasks
        self.done_task1 = Task.objects.create(
            title="Task 1 - Done",
            due_date=date.today() - timedelta(days=2),
            is_completed=True,
            category=self.category_work
        )

    def test_home_view_get_request(self):
        """Test that the home view renders correctly on GET request."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_home_view_displays_todo_tasks(self):
        """Test that the home view displays tasks where is_completed=False."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.todo_task1.title)

    def test_home_view_context_contains_form(self):
        """Test that the context contains the TaskForm."""
        self.client.get(reverse('home'))
        response = self.client.get(reverse('home'))
        self.assertIsInstance(response.context['form'], TaskForm)

# generate a unit test that checks for an error if there are no tasks available in the system
    def test_home_view_no_tasks(self):
        """Test that the home view handles no tasks gracefully."""
        # Delete existing tasks
        Task.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['to_do_tasks']), 0)
        self.assertEqual(len(response.context['done_tasks']), 0)
