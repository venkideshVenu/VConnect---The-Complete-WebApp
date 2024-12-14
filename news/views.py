from django.shortcuts import render, get_object_or_404
from .models import TechArticle
from .services import NewsAPIService

def tech_news_view(request):
    NewsAPIService.fetch_tech_news(max_articles=6)
    articles = TechArticle.objects.order_by('-published_at')[:10]
    return render(request, 'news/tech_news.html', {'articles': articles})


def tech_news_detail_view(request, pk):
    article = get_object_or_404(TechArticle, pk=pk)
    return render(request, 'news/tech_news_detail.html', {
        'article': article
    })