from django.contrib.auth import get_user_model, logout
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from blog_app.accounts.models import Profile

UserModel = get_user_model()
@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_delete, sender=Profile)
# def logout_user_on_profile_delete(sender, instance, **kwargs):
#     if hasattr(instance, 'user') and instance.user.is_authenticated:
#         logout(instance.user)
#--->imported in the app module
