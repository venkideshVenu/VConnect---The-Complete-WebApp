from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobprofile.forms import ProfileForm, SkillForm
from .models import Profile

@login_required
def select_type(request):
    """
    View to allow users to select their account type (Employer or Employee).
    """
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Redirect only if the user has already selected an account type
    if profile.is_employer is not None:
        return redirect('jobprofile:complete_profile')

    if request.method == 'POST':
        account_type = request.POST.get('type')
        if account_type in ['employer', 'employee']:
            profile.is_employer = (account_type == 'employer')
            profile.save()

            # Add a success message
            messages.success(request, f'Profile type set as {account_type.title()}')
            return redirect('jobprofile:complete_profile')
        else:
            messages.error(request, 'Invalid account type selected')

    return render(request, 'jobs/select_type.html')

@login_required
def complete_profile(request):
    """
    View to complete the user's profile.
    """
    try:
        profile = request.user.job_profile
    except Profile.DoesNotExist:
        return redirect('jobprofile:select_type')
    
    # Redirect to select_type if type is not selected
    if profile.is_employer is None:
        return redirect('jobprofile:select_type')
    
    is_employer = profile.is_employer  # Get employer status

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, is_employer=is_employer)
        if form.is_valid():
            profile = form.save(commit=False)  # Save the form but don't commit to the database yet
            
            # Dynamically handle `company_name` for employers
            if is_employer:
                profile.company_name = form.cleaned_data.get('company_name', '').strip()

            profile.save()  # Save the profile to the database

            # Check if all required fields are completed
            required_fields = ['location', 'short_intro']
            if is_employer:
                required_fields.append('company_name')

            if all(getattr(profile, field, '').strip() for field in required_fields):
                request.user.mark_profile_section_complete('profile', True)
                messages.success(request, 'Profile completed successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Please fill in all required fields.')
        else:
            messages.error(request, 'Form submission contains errors.')
    else:
        form = ProfileForm(instance=profile, is_employer=is_employer)

    return render(request, 'jobs/complete_profile.html', {
        'form': form,
        'is_employer': is_employer,
    })



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


@login_required
def inbox(request):
    profile = request.user.job_profile

    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'jobs/inbox.html', context)
