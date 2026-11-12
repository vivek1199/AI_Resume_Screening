from django.urls import path

from .views import admin_dashboard, candidate_dashboard

urlpatterns = [
    path("", admin_dashboard, name="dashboard"),
    path(
        "candidate/",
        candidate_dashboard,
        name="candidate_dashboard"
    ),
]