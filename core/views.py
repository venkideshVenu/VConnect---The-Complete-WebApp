from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, CustomPasswordChangeForm
from .forms import CombinedProfileForm


# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Automatically mark the user as verified
            user.is_verified = True
            user.save()
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('homepage') 
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')  # Redirect to login page

@login_required
def profile_view(request):
    """View for displaying user profile"""
    context = {
        'user': request.user,
        'profile': request.user.job_profile,
        'skills': request.user.job_profile.skill_set.all() if hasattr(request.user, 'job_profile') else None
    }
    return render(request, 'core/profile.html', context)

@login_required
def profile_update(request):
    """View for updating user profile"""
    if request.method == 'POST':
        form = CombinedProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CombinedProfileForm(instance=request.user)

    context = {
        'form': form,
        'user': request.user,
        'skills': request.user.job_profile.skill_set.all() if hasattr(request.user, 'job_profile') else None
    }
    return render(request, 'core/profile_update.html', context)

@login_required
def password_change(request):
    """View for changing password"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'core/password_update.html', {'form': form})