from django.shortcuts import redirect
from django.urls import resolve

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path.startswith('/jobs/'):
            excluded_urls = ['select_type', 'complete_profile']
            current_url = resolve(request.path).url_name

            # Skip the middleware logic for excluded URLs
            if current_url in excluded_urls:
                return self.get_response(request)

            try:
                profile = request.user.job_profile

                # Redirect to type selection if no type is selected
                if profile.is_employer is None:
                    return redirect('jobprofile:select_type')

                # Check required fields for profile completion
                required_fields = ['location', 'short_intro']
                if profile.is_employer:
                    required_fields.append('company_name')

                if any(not getattr(profile, field) for field in required_fields):
                    request.user.mark_profile_section_complete('profile', False)
                    return redirect('jobprofile:complete_profile')
                else:
                    request.user.mark_profile_section_complete('profile', True)

            except AttributeError:
                return redirect('jobprofile:select_type')

        return self.get_response(request)
