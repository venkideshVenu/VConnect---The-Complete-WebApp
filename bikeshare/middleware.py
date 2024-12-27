# bikeshare/middleware.py
from django.shortcuts import redirect
from django.urls import resolve
from .models import BikeShareProfile

class BikeShareProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path.startswith('/bikeshare/'):
            excluded_urls = ['select_role', 'profile_setup']
            current_url = resolve(request.path).url_name

            if current_url in excluded_urls:
                return self.get_response(request)

            try:
                # Use the correct related name
                profile = request.user.bikeshare_profile
                
                if not profile.role:
                    return redirect('bikeshare:select_role')
                
                request.user.mark_profile_section_complete('bikeshare_profile', True)

            except BikeShareProfile.DoesNotExist:
                return redirect('bikeshare:select_role')

        return self.get_response(request)