# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser): 
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=True)  # Default to True
    profile_completed = models.JSONField(default=dict, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True)
    # Add fields for profile completion tracking
    profile_completed = models.JSONField(default=dict, blank=True)
    
    def mark_profile_section_complete(self, section):
        """
        Mark a specific profile section as complete
        """
        completed = self.profile_completed or {}
        completed[section] = True
        self.profile_completed = completed
        self.save()
    
    def is_section_profile_complete(self, section):
        """
        Check if a specific profile section is complete
        """
        return self.profile_completed.get(section, False)