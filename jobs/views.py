
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import JobForm
from .models import Job


# Check whether the logged-in user is an admin
def is_admin(user):
    return user.is_authenticated and (
        user.is_staff or user.is_superuser
    )


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="candidate_dashboard")
def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("job_list")
    else:
        form = JobForm()

    context = {"form": form}

    return render(request, "jobs/add_job.html", context)


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="candidate_dashboard")
def job_list(request):
    jobs = Job.objects.all().order_by("-id")

    total_jobs = Job.objects.count()
    open_jobs = Job.objects.filter(status="Open").count()
    closed_jobs = Job.objects.filter(status="Closed").count()

    context = {
        "jobs": jobs,
        "total_jobs": total_jobs,
        "open_jobs": open_jobs,
        "closed_jobs": closed_jobs,
    }

    return render(request, "jobs/list.html", context)


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="candidate_dashboard")
def edit_job(request, id):
    job = get_object_or_404(Job, id=id)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect("job_list")
    else:
        form = JobForm(instance=job)

    context = {
        "form": form,
        "job": job,
    }

    return render(request, "jobs/edit_job.html", context)


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="candidate_dashboard")
def delete_job(request, id):
    job = get_object_or_404(Job, id=id)

    if request.method == "POST":
        job.delete()
        return redirect("job_list")

    return render(
        request,
        "jobs/delete_job.html",
        {"job": job},
    )
