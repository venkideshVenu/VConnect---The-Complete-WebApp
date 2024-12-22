from django.urls import path, include
from . import views

app_name = 'learning_centre'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('about/', views.aboutLearn, name='about_learn'),
    path('search', views.SearchView.as_view(), name='search'),
    path('courses/', views.courses, name='courses'),
    path('users/', include([
        path('my-courses', views.EnrolledCoursesListView.as_view(), name='enrolled-courses'),
        path('my-courses/<slug:slug>/view', views.StartLessonView.as_view(), name='course-lessons'),
        path('my-courses/<slug:slug>/lessons/<int:id>', views.LessonView.as_view(), name='course-lessons-single'),
    ])),
]
