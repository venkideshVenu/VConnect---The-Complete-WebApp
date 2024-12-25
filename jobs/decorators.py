from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def employer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.job_profile.is_employer:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Only employers can access this page')
        return redirect('jobs:jobs')
    return wrapper

def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.job_profile.is_employer:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Only job seekers can access this page')
        return redirect('jobs:jobs')
    return wrapper