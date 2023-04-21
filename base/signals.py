from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.utils.text import slugify
from .models import Projects


@receiver(pre_save,sender=Projects)
def create_project(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        

