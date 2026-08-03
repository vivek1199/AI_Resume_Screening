from django.db import models


class Job(models.Model):

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Closed", "Closed"),
    ]

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    experience = models.PositiveIntegerField()

    salary = models.CharField(max_length=100)

    skills = models.TextField()

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title