from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tasks")

    def save(self, *args, **kwargs):
        if len(self.title) > 200:
            raise ValidationError("Title cannot be longer than 200 characters")
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # Enforce model field validation (e.g., title max_length) on save
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (Done)" if self.is_completed else self.title
