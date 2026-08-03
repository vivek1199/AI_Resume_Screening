from django.shortcuts import render, redirect

from .forms import CandidateForm
from .models import Candidate

from nlp_engine.pdf_parser import extract_text_from_pdf
from nlp_engine.matcher import calculate_match

from nlp_engine.skill_extractor import extract_skills
from nlp_engine.analyzer import analyze_resume

from jobs.models import Job


def upload_candidate(request):

    if request.method == "POST":

        form = CandidateForm(request.POST, request.FILES)

        if form.is_valid():

            candidate = form.save(commit=False)

            candidate.save()

            # Get uploaded resume path
            resume_path = candidate.resume.path

            # Extract text from PDF
            resume_text = extract_text_from_pdf(resume_path)

            # Save extracted text
            candidate.extracted_text = resume_text

            # Extract skills from resume
            resume_skills = extract_skills(resume_text)

            # Save extracted skills
            candidate.extracted_skills = ", ".join(resume_skills)

            # Analyze resume against job skills
            analysis = analyze_resume(
                candidate.job.skills,
                resume_skills
            )
            print("=" * 50)
            print("Resume Text:")
            print(resume_text)

            print("=" * 50)
            print("Resume Skills:")
            print(resume_skills)

            print("=" * 50)
            print("Job Skills:")
            print(candidate.job.skills)

            print("=" * 50)
            print("Analysis:")
            print(analysis)
            print("=" * 50)
            # Save AI results
            candidate.ai_score = analysis["score"]
            candidate.matched_skills = ", ".join(analysis["matched"])
            candidate.missing_skills = ", ".join(analysis["missing"])
            candidate.recommendation = analysis["recommendation"]

            candidate.save()

            return redirect("candidate_list")

    else:

        form = CandidateForm()

    return render(
        request,
        "candidates/upload.html",
        {
            "form": form
        }
    )
    
from .models import Candidate

def candidate_list(request):

    candidates = Candidate.objects.all().order_by("-ai_score")

    return render(
        request,
        "candidates/list.html",
        {
            "candidates": candidates
        }
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