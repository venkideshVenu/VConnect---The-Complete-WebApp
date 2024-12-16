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

            # Use a set to keep track of unique articles
            existing_hashes = set(
                TechArticle.objects.values_list("url", flat=True)
            )
            
            articles_to_save = []

            for article_data in news_data.get('articles', [])[:max_articles]:
                # Extract required fields
                title = article_data.get('title', '')
                description = article_data.get('description', '')
                url = article_data.get('url', '')
                content = article_data.get('content', '')
                image_url = article_data.get('urlToImage', '')
                author = article_data.get('author', '')
                published_at = parse_datetime(article_data.get('publishedAt', datetime.now().isoformat()))
                source = article_data.get('source', {}).get('name', '')

                # Check if article URL is unique
                if url and url not in existing_hashes:
                    # Add article to the list for bulk creation
                    articles_to_save.append(
                        TechArticle(
                            title=title,
                            description=description,
                            url=url,
                            full_content=content,
                            image_url=image_url,
                            author=author,
                            published_at=published_at,
                            source=source
                        )
                    )
                    existing_hashes.add(url)

            # Bulk save new articles
            if articles_to_save:
                TechArticle.objects.bulk_create(articles_to_save)

            # Return last `max_articles` rows from the database
            return TechArticle.objects.order_by('-published_at')[:max_articles]

        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []