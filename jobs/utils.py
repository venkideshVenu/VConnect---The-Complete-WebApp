from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateJobs(request,jobs,results):
    page = request.GET.get('page')
    results = 3
    paginator = Paginator(jobs, results)

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        jobs = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        jobs = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range,jobs



from .models import JobModel
from django.db.models import Q

def searchJobs(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # Filter parameters
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')
    experience = request.GET.get('experience', '')
    posted_within = request.GET.get('posted_within', '')
    salary_min = request.GET.get('salary_min', '')
    salary_max = request.GET.get('salary_max', '')
    
    # Base query
    jobs = JobModel.objects.distinct()
    
    # Search query filter
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        )
    
    # Apply other filters
    if job_type:
        jobs = jobs.filter(type=job_type)
    
    if location:
        jobs = jobs.filter(location__icontains=location)
        
    if salary_min and salary_max:
        jobs = jobs.filter(
            salary_range__regex=fr'^[\$]?([{salary_min}-{salary_max}]+)'
        )
    
    return jobs, search_query