"""
URL configuration for VConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('start/', include('core.urls')),
    path('news/', include('news.urls')),
    path('learn/', include('learning_centre.urls')),
    path('courses/', include('courses.urls')),
    path('cart/', include('cart.urls')),
    path('tasks/', include('tasks.urls')),
    path('jobprofile/', include('jobprofile.urls')),
    path('jobs/', include('jobs.urls')),
    path('bikeshare/', include('bikeshare.urls')),
    path('socialhub/', include('socialhub.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
