from django.test import TestCase
from datetime import date, timedelta
from .forms import TaskForm
from .models import Task, Category


class TaskFormTestCase(TestCase):
    """Test cases for the TaskForm."""

    def setUp(self):
        """Set up test data before each test."""
        # Create test categories
        self.category_work = Category.objects.create(name="Work")
        self.category_personal = Category.objects.create(name="Personal")

        # Valid form data for testing
        self.valid_form_data = {
            'title': 'Test Task',
            'due_date': date.today() + timedelta(days=7),
            'category': self.category_work.id,
        }

        # Form data with missing required fields
        self.invalid_form_data_no_title = {
            'due_date': date.today() + timedelta(days=7),
            'category': self.category_work.id,
        }

        self.invalid_form_data_no_category = {
            'title': 'Test Task',
            'due_date': date.today() + timedelta(days=7),
        }

    def test_task_form_valid_data(self):
        """Test that the form is valid with correct data."""
        form = TaskForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_category(self):
        """Test that an invalid category makes the form invalid."""
        self.valid_form_data['category'] = 9999
        form = TaskForm(data=self.valid_form_data)
        self.assertFalse(form.is_valid())

    def test_task_form_empty_submission(self):
        """Test that an empty form submission is invalid."""
        self.valid_form_data = {}
        form = TaskForm(data=self.valid_form_data)
        self.assertFalse(form.is_valid())


# edge cases, for example, when the task title length is too long

    def test_task_form_title_too_long(self):
        """Test that a title exceeding max length makes the form invalid."""
        self.valid_form_data['title'] = 'T' * 201
        form = TaskForm(data=self.valid_form_data)
        self.assertFalse(form.is_valid())
