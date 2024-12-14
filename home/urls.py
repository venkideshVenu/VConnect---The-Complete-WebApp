from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.get_home_page, name="homepage"),
    # path('about/', views.about, name='about'),
    #path('contact/', views.contact, name='contact'),
    #path('notfound/', views.errorpage, name='notfound'),
    #path('twenty20/', views.twenty20, name='twenty20'),
    #path('odi/', views.odi, name='odi'),
    #path('testChampionship/', views.test, name='test'),
]