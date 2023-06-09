from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save,sender= User)
def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            username=user.username,
            name = user.first_name,
            email = user.email,
        )

@receiver(post_save,sender= Profile)
def update_profile(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.username = profile.username
        user.first_name = profile.name
        user.email = profile.email
        user.save()


@receiver(post_delete,sender=Profile)
def delete_user(sender, instance, *args,**kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


