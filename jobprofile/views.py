from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobprofile.forms import ProfileForm, SkillForm

@login_required
def select_type(request):
    """
    View to allow users to select their account type (Employer or Employee).
    """
    profile = getattr(request.user, 'job_profile', None)
    if not profile:
        from jobprofile.models import Profile
        profile = Profile.objects.create(user=request.user)

    if profile.is_employer is not None:
        return redirect('jobprofile:profile')

    if request.method == 'POST':
        account_type = request.POST.get('type')
        if account_type:
            profile.is_employer = account_type == 'employer'
            profile.save()
            return redirect('jobprofile:complete_profile')

    return render(request, 'jobs/select_type.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobprofile.forms import ProfileForm

@login_required
def complete_profile(request):
    """
    View to complete the user's profile, including role selection (Employer or Job Seeker).
    """
    profile = getattr(request.user, 'job_profile', None)
    if not profile:
        from jobprofile.models import Profile
        profile = Profile.objects.create(user=request.user)

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, 'Profile completed successfully!')
            return redirect('jobprofile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'jobs/complete_profile.html', {'form': form})


@login_required
def profile(request):
    """
    View to display the user's profile.
    """
    profile = getattr(request.user, 'job_profile', None)
    if not profile:
        return redirect('jobprofile:select_type')

    context = {
        'profile': profile,
        'skills': profile.skill_set.all() if not profile.is_employer else None
    }
    return render(request, 'jobs/profile.html', context)

@login_required
def add_skill(request):
    """
    View to add skills to the user's profile.
    """
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.job_profile
            skill.save()
            return redirect('jobprofile:profile')
    else:
        form = SkillForm()
    return render(request, 'jobs/skill_form.html', {'form': form})
