from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import date, timedelta
from .models import Task, Category


class TaskModelTest(TestCase):
    """Test suite for the Task model"""

    def setUp(self):
        """Set up test data before each test method"""
        # Create a test category
        self.category = Category.objects.create(name="Work")

        # Create a test task
        self.task = Task.objects.create(
            title="Test Task",
            due_date=date.today() + timedelta(days=7),
            is_completed=False,
            category=self.category
        )

    def test_task_creation(self):
        """Test that a task can be created"""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.due_date, date.today() + timedelta(days=7))
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.category, self.category)

    def test_task_str_method(self):
        """
        Test the __str__ method of the Task model to ensure it returns the correct
        string representation. Verifies that:
        1. An incomplete task returns its title as the string representation
        2. A completed task appends "(Done)" to the title in the string representation
        """

        self.assertEqual(str(self.task), "Test Task")

    def test_task_default_is_completed(self):
        """Test that is_completed defaults to False"""
        new_task = Task.objects.create(
            title="Another Test Task",
            due_date=date.today() + timedelta(days=5),
            category=self.category
        )
        self.assertFalse(new_task.is_completed)

    def test_task_category_relationship(self):
        """Test the foreign key relationship with Category"""
        self.assertEqual(self.task.category.name, "Work")

    def test_task_due_date_optional(self):
        """Test that due_date can be null"""
        self.task.due_date = None
        self.task.save()
        self.assertIsNone(self.task.due_date)

    def test_task_title_max_length(self):
        """Test that titles longer than 200 characters fail validation"""
        task = Task(
            title="T" * 201,
            due_date=date.today() + timedelta(days=7),
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            task.save()
