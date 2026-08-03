from django.shortcuts import render, redirect
from .forms import JobForm
from .models import Job
from django.shortcuts import get_object_or_404

def add_job(request):

    if request.method == "POST":

        form = JobForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("job_list")

    else:

        form = JobForm()

    context = {
        "form": form
    }

    return render(request, "jobs/add_job.html", context)

def job_list(request):

    jobs = Job.objects.filter(status="Open")

    return render(
        request,
        "jobs/list.html",
        {
            "jobs": jobs
        }
    )
    
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

    return render(
        request,
        "jobs/edit_job.html",
        context,
    )
    
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