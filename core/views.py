from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
# core/views.py
from django.contrib import messages

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

# User Dashboard View
def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to log in first.')
        return redirect('login')
    return render(request, 'core/dashboard.html', {'user': request.user})
