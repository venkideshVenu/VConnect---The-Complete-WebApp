from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from courses.models import Category, Lesson, Course
from .models import Enroll

def index(request):
    category = Category.objects.all()
    return render(request, 'learn/index.html', {'category': category})

def aboutLearn(request):
    return render(request, 'learn/about.html', {})

def courses(request):
    courses = Course.objects.all()
    return render(request, 'learn/courses.html', {'courses': courses})

class HomeListView(ListView):
    model = Course
    template_name = 'learn/index.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['top_courses'] = self.model.objects.all().order_by('?')
        return context

class SearchView(ListView):
    model = Course
    template_name = 'learn/search.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(title__contains=self.request.GET['q'])

class EnrolledCoursesListView(ListView):
    model = Enroll
    template_name = 'courses/enrolled_courses.html'
    context_object_name = 'enrolls'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('course').filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def transform_video_url(url):
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('watch?v=')[1].split('&')[0]
        return f"https://www.youtube.com/embed/{video_id}?autoplay=0&rel=0"
    return url

class StartLessonView(DetailView):
    model = Lesson
    template_name = 'courses/lessons_by_course.html'
    context_object_name = 'current_lesson'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        queryset = queryset.filter(course=course)
        try:
            obj = queryset.first()
            if not obj:
                raise Http404("No lessons found for this course")
            obj.video_url = transform_video_url(obj.video_url)
            return obj
        except queryset.model.DoesNotExist:
            raise Http404("Lesson not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        lessons = self.model.objects.filter(course=course)
        for lesson in lessons:
            lesson.video_url = transform_video_url(lesson.video_url)
        context["lessons"] = lessons
        context["course"] = course
        return context

class LessonView(DetailView):
    model = Lesson
    template_name = 'courses/lessons_by_course.html'
    context_object_name = 'current_lesson'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lesson_id = self.kwargs['id']
        queryset = queryset.filter(id=lesson_id)
        try:
            obj = queryset.get()
            obj.video_url = transform_video_url(obj.video_url)
            return obj
        except queryset.model.DoesNotExist:
            raise Http404("Lesson not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        lessons = self.model.objects.filter(course=course)
        for lesson in lessons:
            lesson.video_url = transform_video_url(lesson.video_url)
        context["lessons"] = lessons
        context["course"] = course
        return context