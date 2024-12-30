from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import JobForm, ApplyJobForm
from .utils import searchJobs, paginateJobs
from .models import JobModel, ApplicantModel
from jobprofile.models import Profile


def index(request):
    jobs, search_query = searchJobs(request)
    custom_range, jobs = paginateJobs(request, jobs, 6)

    context = {'jobs': jobs, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'jobs/index.html', context)

def jobs(request):
    jobs, search_query = searchJobs(request)
    job_count = jobs.count()
    
    context = {
        'jobs': jobs, 
        'search_query': search_query,
        'job_count': job_count
    }
    return render(request, 'jobs/jobs_listing.html', context)


def job(request, pk):
    job = get_object_or_404(JobModel, id=pk)
    tags = job.tags.all()
    
    already_applied = False
    if request.user.is_authenticated:
        profile = request.user.job_profile
        already_applied = ApplicantModel.objects.filter(user=profile, job=job).exists()

    context = {
        'job': job,
        'tags': tags,
        'already_applied': already_applied
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def createJob(request):
    profile = request.user.job_profile
    
    # Only employers can create jobs
    if not profile.is_employer:
        messages.error(request, 'Only employers can create job listings')
        return redirect('jobs:jobs')
        
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = profile
            job.save()
            form.save_m2m()  # Save tags
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:jobs')
    else:
        form = JobForm()

    context = {'form': form}
    return render(request, 'jobs/job_form.html', context)

@login_required
def updateJob(request, pk):
    profile = request.user.job_profile
    job = get_object_or_404(JobModel, id=pk, owner=profile)
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs:job', pk=job.id)
    else:
        form = JobForm(instance=job)

    context = {'form': form}
    return render(request, 'jobs/job_form.html', context)

@login_required
def deleteJob(request, pk):
    profile = request.user.job_profile
    job = get_object_or_404(JobModel, id=pk, owner=profile)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('jobs:jobs')

    context = {'object': job}
    return render(request, 'jobs/delete_job.html', context)

@login_required
def applyJob(request, pk):
    profile = request.user.job_profile
    job = get_object_or_404(JobModel, id=pk)
    
    # Employers cannot apply for jobs
    if profile.is_employer:
        messages.error(request, 'Employers cannot apply for jobs')
        return redirect('jobs:job', pk=job.id)
    
    # Check if already applied
    if ApplicantModel.objects.filter(user=profile, job=job).exists():
        messages.info(request, 'You have already applied for this job')
        return redirect('jobs:job', pk=job.id)
        
    if request.method == 'POST':
        form = ApplyJobForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = profile
            application.job = job
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('jobs:job', pk=job.id)
    else:
        form = ApplyJobForm()

    context = {'form': form, 'job': job}
    return render(request, 'jobs/apply_form.html', context)

@login_required
def manageCandidates(request):
    profile = request.user.job_profile
    
    # Only employers can view candidates
    if not profile.is_employer:
        messages.error(request, 'Access denied')
        return redirect('jobs:jobs')
        
    jobs = JobModel.objects.filter(owner=profile)
    applications = ApplicantModel.objects.filter(job__in=jobs)
    
    context = {'applications': applications}
    return render(request, 'jobs/manage_candidates.html', context)

@login_required
def myApplications(request):
    profile = request.user.job_profile
    
    # Only job seekers can view their applications
    if profile.is_employer:
        messages.error(request, 'Employers cannot apply for jobs')
        return redirect('jobs:jobs')
        
    applications = ApplicantModel.objects.filter(user=profile)
    context = {'applications': applications}
    return render(request, 'jobs/my_applications.html', context)


@login_required
def createApplyJobview(request, pk):
    profile = request.user.job_profile
    job = get_object_or_404(JobModel, id=pk)
    
    if profile.is_employer:
        messages.error(request, 'Employers cannot apply for jobs')
        return redirect('jobs:job', pk=job.id)
        
    if ApplicantModel.objects.filter(user=profile, job=job).exists():
        messages.info(request, 'You have already applied for this job')
        return redirect('jobs:job', pk=job.id)
        
    if request.method == 'POST':
        application = ApplicantModel.objects.create(
            user=profile,
            job=job
        )
        messages.success(request, 'Application submitted successfully!')
        return redirect('jobs:job', pk=job.id)

    context = {'job': job}
    return render(request, 'jobs/apply_form.html', context)


@login_required()
def allApplicantsView(request):
    applicants = ApplicantModel.objects.all()

    context = {'applicants': applicants}
    return render(request, 'jobs/applicants_list.html', context)


@login_required
def applicantView(request):
    # Get the profile of the logged-in user
    profile = request.user.job_profile
    
    # Get all the applications for this user's profile
    applicants = profile.applicants.all()
    
    # Fetch the jobs associated with these applications
    jobs = [applicant.job for applicant in applicants]
    
    context = {'jobs': jobs}  # Pass the list of jobs to the template
    return render(request, 'jobs/job_applications.html', context)


@login_required()
def appliedApplicantsView(request, pk):
    applicant = ApplicantModel.objects.get(id=pk)

    if applicant.is_read == False:
        applicant.is_read = True
        applicant.save()

    context = {'applicant': applicant}
    return render(request, 'jobs/applied_applicant.html', context)


