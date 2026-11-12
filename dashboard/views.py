from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render
from django.db.models import Avg

from jobs.models import Job
from candidates.models import Candidate


def dashboard(request):

    total_jobs = Job.objects.count()

    open_jobs = Job.objects.filter(
        status="Open"
    ).count()

    total_candidates = Candidate.objects.count()

    shortlisted = Candidate.objects.filter(
        status="Shortlisted"
    ).count()

    rejected = Candidate.objects.filter(
        status="Rejected"
    ).count()

    pending = Candidate.objects.filter(
        status="Pending"
    ).count()

    average_score = Candidate.objects.aggregate(
        average=Avg("ai_score")
    )["average"] or 0

    top_candidates = (
        Candidate.objects.select_related("job")
        .order_by("-ai_score")[:5]
    )

    recent_candidates = (
        Candidate.objects.select_related("job")
        .order_by("-uploaded_at")[:6]
    )

    context = {
        "total_jobs": total_jobs,
        "open_jobs": open_jobs,
        "total_candidates": total_candidates,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "pending": pending,
        "average_score": round(average_score, 1),
        "top_candidates": top_candidates,
        "recent_candidates": recent_candidates,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )

def is_admin(user):
    return user.is_authenticated and (
        user.is_staff or user.is_superuser
    )


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return dashboard(request)


@login_required
def candidate_dashboard(request):
    from jobs.models import Job

    jobs = Job.objects.filter(status="Open")

    return render(
        request,
        "dashboard/candidate_dashboard.html",
        {"jobs": jobs}
    )