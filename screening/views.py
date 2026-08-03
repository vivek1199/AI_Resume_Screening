from django.shortcuts import render
from candidates.models import Candidate


def ranking_list(request):

    candidates = Candidate.objects.all().order_by("-ai_score")

    context = {
        "candidates": candidates
    }

    return render(
        request,
        "screening/rankings.html",
        context
    )