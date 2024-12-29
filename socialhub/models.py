from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from core.models import CustomUser
import os

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True, unique=True, max_length=111)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes', blank=True)
    tagged_users = models.ManyToManyField(CustomUser, related_name='tagged_in_posts', blank=True)

    def save(self, *args, **kwargs):
        # Generate thumbnail when saving
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            
            # Handle image orientation
            try:
                exif = img._getexif()
                if exif:
                    orientation = exif.get(274)  # 274 is the orientation tag
                    if orientation:
                        rotate_values = {
                            3: 180,
                            6: 270,
                            8: 90
                        }
                        if orientation in rotate_values:
                            img = img.rotate(rotate_values[orientation], expand=True)
            except (AttributeError, KeyError, IndexError):
                # No EXIF data available or no orientation info
                pass

            # Resize image
            output_size = (1000, 500)
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
            
            # If image is smaller than target size, create white background
            if img.size != output_size:
                background = Image.new('RGB', output_size, 'white')
                # Calculate position to paste the image centered
                offset = ((output_size[0] - img.size[0]) // 2,
                         (output_size[1] - img.size[1]) // 2)
                background.paste(img, offset)
                img = background

            # Save the processed image
            img.save(self.image.path, quality=70, optimize=True)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('socialhub:post-detail', kwargs={'slug': self.slug})

    def whatsapp_share_url(self):
        url = f"https://wa.me/?text=http://yourdomain.com{self.get_absolute_url()}"
        return url

    def facebook_share_url(self):
        url = f"https://www.facebook.com/sharer/sharer.php?u=http://yourdomain.com{self.get_absolute_url()}"
        return url

    def twitter_share_url(self):
        url = f"https://twitter.com/intent/tweet?text=http://yourdomain.com{self.get_absolute_url()}"
        return url

REASON_CHOICES = [
    ('SPAM', 'SPAM'),
    ('INAPPROPRIATE', 'INAPPROPRIATE'),
]

class PostReport(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.CharField(max_length=13, choices=REASON_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.post.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

class Notification(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    action = models.CharField(max_length=50, blank=True)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']



from django.db import models
from django.utils import timezone
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser
from taggit.managers import TaggableManager

# Add this at the top of your models.py
WING = [
    ('Army', 'Army'),
    ('Navy', 'Navy'),
    ('Air Force', 'Air Force')
]

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=25, blank=True)
    description = models.CharField(max_length=100, blank=True)
    follows = models.ManyToManyField(CustomUser, related_name="profile_follows", blank=True)
    followers = models.ManyToManyField(CustomUser, related_name="profile_followers", blank=True)
    camps = TaggableManager(blank=True)
    wing = models.CharField(max_length=10, choices=WING, blank=True)

    @property
    def name(self):
        # Combine the first and last name of the related CustomUser
        return f"{self.user.first_name} {self.user.last_name}".strip()
    

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Process the user's profile picture from CustomUser
        if self.user.profile_picture:
            img = Image.open(self.user.profile_picture.path)
            
            # Handle image orientation
            try:
                exif = img._getexif()
                if exif:
                    orientation = exif.get(274)
                    if orientation:
                        rotate_values = {
                            3: 180,
                            6: 270,
                            8: 90
                        }
                        if orientation in rotate_values:
                            img = img.rotate(rotate_values[orientation], expand=True)
            except (AttributeError, KeyError, IndexError):
                pass

            # Resize to thumbnail size
            output_size = (170, 170)
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
            
            # Create square image with white background
            background = Image.new('RGB', output_size, 'white')
            offset = ((output_size[0] - img.size[0]) // 2,
                     (output_size[1] - img.size[1]) // 2)
            background.paste(img, offset)
            
            # Save the processed image
            background.save(self.user.profile_picture.path, quality=100, optimize=True)

class UserReport(models.Model):
    reported_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reported_user')
    reason = models.CharField(max_length=13, choices=REASON_CHOICES)  # Using the same REASON_CHOICES from above
    reporting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reporting_user')
    date_reported = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.reported_user.username

