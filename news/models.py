from django.db import models

class TechArticle(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    url = models.URLField(max_length=1000)
    published_at = models.DateTimeField()
    source = models.CharField(max_length=200)
    image_url = models.URLField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']