
from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Candidate(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
    )

    # Connect candidate record with registered user
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidate_applications"
    )

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    resume = models.FileField(upload_to="resumes/")

    extracted_text = models.TextField(blank=True)

    extracted_skills = models.TextField(blank=True)

    matched_skills = models.TextField(blank=True)

    missing_skills = models.TextField(blank=True)

    recommendation = models.CharField(
        max_length=50,
        default="Pending"
    )

    ai_score = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
