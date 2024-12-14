from django.db import models
from django.urls import reverse


class TechArticle(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    url = models.URLField(max_length=1000, unique=True)  # Ensure URL uniqueness
    published_at = models.DateTimeField()
    source = models.CharField(max_length=200)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    full_content = models.TextField(null=True, blank=True)  # Optional: if you want to store full article content
    author = models.CharField(max_length=200, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('tech_news_detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']
