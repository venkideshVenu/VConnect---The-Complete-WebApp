from django.urls import path
from . import views

urlpatterns = [
    path('', views.tech_news_view, name='tech_news'),
]