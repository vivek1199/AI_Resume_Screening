from django.shortcuts import render

from jobs.models import Job
from candidates.models import Candidate


def dashboard(request):

    total_jobs = Job.objects.count()

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

    top_candidates = Candidate.objects.order_by(
        "-ai_score"
    )[:5]

    recent_candidates = Candidate.objects.order_by(
        "-uploaded_at"
    )[:5]

    context = {

        "total_jobs": total_jobs,

        "total_candidates": total_candidates,

        "shortlisted": shortlisted,

        "rejected": rejected,

        "pending": pending,

        "top_candidates": top_candidates,

        "recent_candidates": recent_candidates,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )   