from django.db import models
from django.conf import settings
from PIL import Image
import uuid

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_profile')
    is_employer = models.BooleanField(null=True, blank=True)
    gender_choices = [("F", "Female"), ("M", "Male")]
    gender = models.CharField(choices=gender_choices, max_length=5, null=True, blank=True)
    education_choices = [
        ("1", "High School"), 
        ("2", "Associate Degree"), 
        ("3", "License"), 
        ("4", "Postgraduate"), 
        ("5", "Doctor")
    ]
    education = models.CharField(choices=education_choices, max_length=13, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)  # For employers
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.user.email} ({'Employer' if self.is_employer else 'Employee'})"

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = 'Messages'
        ordering = ['is_read','-created']

    def __str__(self):
        return self.subject
