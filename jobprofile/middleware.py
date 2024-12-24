from django.shortcuts import redirect
from django.urls import resolve

class ProfileCompletionMiddleware:
    """
    Middleware to ensure the user's profile is complete before accessing job-related pages.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path.startswith('/jobs/'):
            excluded_urls = ['select_type', 'complete_profile']
            current_url = resolve(request.path).url_name

            try:
                # Check if the user has a Profile
                profile = request.user.job_profile

                # Redirect to type selection if account type is not set
                if profile.is_employer is None:
                    return redirect('jobprofile:select_type')

                # Check required fields for profile completion
                required_fields = ['location', 'short_intro']
                if profile.is_employer:
                    required_fields.append('company_name')

                if any(not getattr(profile, field, None) for field in required_fields):
                    if current_url not in excluded_urls:
                        return redirect('jobprofile:complete_profile')

            except AttributeError:
                # Redirect if the profile is missing
                return redirect('jobprofile:select_type')

        # Proceed with the normal request flow
        response = self.get_response(request)
        return response
