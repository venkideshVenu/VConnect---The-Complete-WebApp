from django.urls import path
from .views import tech_news_view, tech_news_detail_view, old_tech_news_view

urlpatterns = [
    path('', tech_news_view, name='tech_news'),
    path('old/', old_tech_news_view, name='old_tech_news'),
    path('<int:pk>/', tech_news_detail_view, name='tech_news_detail'),
]
