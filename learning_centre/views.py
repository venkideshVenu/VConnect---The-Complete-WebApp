from django.shortcuts import render
from django.views.generic import ListView

from courses.models import Course, Category


def index(request):
    return render(request, 'learn/index.html', {})

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
        context['top_courses'] = self.model.objects.all().order_by('?')
        return context


class SearchView(ListView):
    model = Course
    template_name = 'learn/search.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(title__contains=self.request.GET['q'])





from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, RedirectView, ListView, DetailView, UpdateView

from courses.models import Category, Lesson, Course
from .models import Enroll


class EnrolledCoursesListView(ListView):
    model = Enroll
    template_name = 'learn/courses/enrolled_courses.html'
    context_object_name = 'enrolls'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('course').filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class StartLessonView(DetailView):
    model = Lesson
    template_name = 'learn/lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        queryset = queryset.filter(course=course)
        try:
            # Get the single item from the filtered queryset
            obj = queryset[:1].get()
            url = obj.video_url
            url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        return context


class LessonView(DetailView):
    model = Lesson
    template_name = 'learn/lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lesson_id = self.kwargs['id']
        queryset = queryset.filter(id=lesson_id)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            url = obj.video_url
            url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        return context
