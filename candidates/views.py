from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CandidateForm
from .models import Candidate
from jobs.models import Job

from nlp_engine.pdf_parser import extract_text_from_resume
from nlp_engine.skill_extractor import extract_skills
from nlp_engine.analyzer import analyze_resume


@login_required(login_url="login")
def upload_candidate(request):

    if request.method == "POST":

        form = CandidateForm(request.POST, request.FILES)

        if form.is_valid():

            candidate = form.save(commit=False)

            # Connect the application to the logged-in candidate.
            # Admin uploads are not treated as admin applications.
            if not (request.user.is_staff or request.user.is_superuser):
                candidate.user = request.user

            candidate.save()

            saved_file = candidate.resume.name

            try:
                # Extract resume text
                resume_text = extract_text_from_resume(
                    candidate.resume.path
                )

                # Detect candidate skills
                resume_skills = extract_skills(resume_text)

                # Analyze against the selected job
                analysis = analyze_resume(
                    candidate.job.skills,
                    resume_skills,
                    candidate.job.description,
                    resume_text
                )

                # Save analysis results
                candidate.extracted_text = resume_text
                candidate.extracted_skills = ", ".join(resume_skills)

                candidate.matched_skills = ", ".join(
                    analysis["matched"]
                )

                candidate.missing_skills = ", ".join(
                    analysis["missing"]
                )

                candidate.ai_score = analysis["score"]
                candidate.recommendation = analysis["recommendation"]

                candidate.save()

                messages.success(
                    request,
                    "Resume analyzed successfully!"
                )

                if request.user.is_staff or request.user.is_superuser:
                    return redirect("candidate_list")

                return redirect("candidate_dashboard")

            except Exception as error:

                candidate.resume.storage.delete(saved_file)
                candidate.delete()

                messages.error(
                    request,
                    f"Resume processing failed: {error}"
                )

        else:
            messages.error(
                request,
                "Please correct the errors in the form."
            )

    else:
        form = CandidateForm()

    return render(
        request,
        "candidates/upload.html",
        {"form": form}
    )

from .models import Candidate


def candidate_list(request):

    candidates = Candidate.objects.select_related(
        "job"
    ).order_by("-ai_score")

    total_candidates = Candidate.objects.count()

    shortlisted_count = Candidate.objects.filter(
        status="Shortlisted"
    ).count()

    pending_count = Candidate.objects.filter(
        status="Pending"
    ).count()

    context = {
        "candidates": candidates,
        "total_candidates": total_candidates,
        "shortlisted_count": shortlisted_count,
        "pending_count": pending_count,
    }

    return render(
        request,
        "candidates/list.html",
        context
    )
   
from django.shortcuts import get_object_or_404

def candidate_detail(request, id):

    candidate = get_object_or_404(
        Candidate,
        id=id
    )

    context = {
        "candidate": candidate
    }

    return render(
        request,
        "candidates/detail.html",
        context
    )
    
def apply_candidate(request):

    job_id = request.GET.get("job")

    job = Job.objects.get(id=job_id)

    form = CandidateForm(
        initial={
            "job": job
        }
    )

    context = {
        "form": form,
        "job": job,
    }

    return render(
        request,
        "candidates/apply.html",
        context,
    )
    
def apply(request):

    form = CandidateForm()

    job_id = request.GET.get("job")

    if job_id:

        form.fields["job"].initial = job_id

    return render(
        request,
        "candidates/apply.html",
        {
            "form": form
        }
    )