from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [

    path("admin/", admin.site.urls),

    # Landing Page
    path(
        "",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),

    # Accounts
    path("", include("accounts.urls")),

    # Dashboard
    path("dashboard/", include("dashboard.urls")),

    # Jobs
    path("jobs/", include("jobs.urls")),

    # Candidates
    path("candidates/", include("candidates.urls")),

    # Rankings
    path("ranking/", include("screening.urls")),

]