from django.urls import path
from . import views

app_name = 'jobprofile'

urlpatterns = [
    path('select-type/', views.select_type, name='select_type'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('inbox/',views.inbox,name='inbox'),
]