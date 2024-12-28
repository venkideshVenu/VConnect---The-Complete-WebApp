from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from core.models import CustomUser
from .models import Post, Comment, Notification
from socialhub.models import Profile

@receiver(post_save, sender=Post)
def post_mentioned_notify(sender, instance, created, **kwargs):
    if created:
        sender_user = CustomUser.objects.get(pk=instance.author.pk)
        post = instance
        string = instance.content
        poss_users = [i for i in string.split() if i.startswith("@")]
        poss_users_list = [user[1:] for user in poss_users]

        for username in poss_users_list:
            try:
                get_user = CustomUser.objects.get(username=username)
                if get_user not in instance.tagged_users.all() and get_user != sender_user:
                    instance.tagged_users.add(get_user)
                    Notification.objects.create(
                        sender=sender_user,
                        receiver=get_user,
                        post=post,
                        action="mentioned you in post"
                    )
            except CustomUser.DoesNotExist:
                continue

@receiver(post_save, sender=Comment)
def comment_added_notify(sender, instance, created, **kwargs):
    if created:
        sender_user = instance.author
        post = instance.post
        receiver = post.author
        if receiver != sender_user:
            Notification.objects.create(
                sender=sender_user,
                receiver=receiver,
                post=post,
                action="commented on your post"
            )

@receiver(pre_save, sender=Post)
def slug_generator(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.title} {sender.objects.count()}")



from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from core.models import CustomUser
from .models import Post, Comment, Notification, Profile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile instance when a new CustomUser is created"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Save the Profile instance whenever the CustomUser is saved"""
    instance.profile.save()

