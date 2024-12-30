from django.shortcuts import render, redirect
from news.models import TechArticle
from news.services import NewsAPIService
from django.core.cache import cache
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
import os
def get_home_page(request):
    cached_articles = cache.get('tech_news_articles')
    
    if not cached_articles:
        NewsAPIService.fetch_tech_news(max_articles=3)

        articles = TechArticle.objects.order_by('-published_at')[:3]
        cache.set('tech_news_articles', articles, 3600)
    else:
        articles = cached_articles
      
    return render(request, 'home/index.html', {'articles': articles})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            service = form.cleaned_data['service']
            message = form.cleaned_data['message']
            
            email_subject = f"[{service}] {subject}"
            email_message = f"""
            New contact form submission:
            
            Name: {name}
            Email: {email}
            Service: {service}
            Message:
            {message}
            """
            try:
                send_mail(
                    email_subject,
                    email_message,
                    os.getenv('DEFAULT_FROM_EMAIL'),
                    [os.getenv('CONTACT_EMAIL')],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')
            except Exception as e:
                messages.error(request, 'An error occurred while sending your message. Please try again later.')
    else:
        form = ContactForm()
    
    return render(request, 'home/contact.html', {'form': form})

def about_view(request):
    return render(request, 'home/about.html')