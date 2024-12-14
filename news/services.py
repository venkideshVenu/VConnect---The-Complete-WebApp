import os
from datetime import date, timedelta, datetime
import requests
from django.utils.dateparse import parse_datetime
from dotenv import load_dotenv
from .models import TechArticle

load_dotenv()

class NewsAPIService:
    @staticmethod
    def fetch_tech_news(max_articles=10):
        api_key = os.getenv('NEWS_API_KEY')
        base_url = 'https://newsapi.org/v2/everything'
        
        yesterday = date.today() - timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d')

        params = {
            'q': 'technology',  # Search query
            'from': yesterday,      # Articles from yesterday
            'sortBy': 'popularity',
            'apiKey': api_key,
            'pageSize': max_articles
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            news_data = response.json()
            
            articles = []
            for article_data in news_data.get('articles', [])[:max_articles]:
                article = TechArticle(
                    title=article_data.get('title', ''),
                    description=article_data.get('description', ''),
                    url=article_data.get('url', ''),
                    published_at=parse_datetime(article_data.get('publishedAt', datetime.now().isoformat())),
                    source=article_data.get('source', {}).get('name', ''),
                    image_url=article_data.get('urlToImage')
                )
                articles.append(article)
            
            # Bulk create articles to reduce database queries
            TechArticle.objects.bulk_create(articles, ignore_conflicts=True)
            
            return articles
        
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []