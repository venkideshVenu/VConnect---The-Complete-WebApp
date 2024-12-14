
from django.shortcuts import render
from .models import TechArticle

from django.core.cache import cache
'''
def tech_news_view(request):
    # Try to get cached articles
    cached_articles = cache.get('tech_news_articles')
    
    if not cached_articles:
        # Fetch new articles if not in cache
        articles = WebzIOService.fetch_tech_news(max_articles=6)
        
        # Cache the articles for 1 hour
        cache.set('tech_news_articles', articles, 3600)
    else:
        articles = cached_articles
    
    return render(request, 'news/tech_news.html', {
        'articles': articles
    })
'''
from django.shortcuts import render
from .services import NewsAPIService
from .models import TechArticle

def tech_news_view(request):
    # Fetch and save latest tech news, explicitly limiting to 10
    articles = NewsAPIService.fetch_tech_news(max_articles=3)
    
    return render(request, 'news/tech_news.html', {
        'articles': articles
    })