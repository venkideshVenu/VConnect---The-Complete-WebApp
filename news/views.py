from django.shortcuts import render, get_object_or_404
from .models import TechArticle
from .services import NewsAPIService
from django.core.cache import cache

def tech_news_view(request):
    cached_articles = cache.get('tech_news_articles')
    
    if not cached_articles:
        # Fetch new articles if not in cache
        NewsAPIService.fetch_tech_news(max_articles=9)

        articles = TechArticle.objects.order_by('-published_at')[:12]
        # Cache the articles for 1 hour
        cache.set('tech_news_articles', articles, 3600)
    else:
        articles = cached_articles
      
    return render(request, 'news/tech_news.html', {'articles': articles})


def old_tech_news_view(request):
    articles = TechArticle.objects.order_by('-published_at')[6:18]
    return render(request, 'news/old_news.html', {'articles': articles})


def tech_news_detail_view(request, pk):
    article = get_object_or_404(TechArticle, pk=pk)
    return render(request, 'news/tech_news_detail.html', {
        'article': article
    })