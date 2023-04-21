from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=60,null=True,blank=True)
    username = models.CharField(max_length=60,null=True,blank=True)
    domain = models.CharField(max_length=60,blank=True)
    email = models.EmailField(max_length=250,blank=True)
    avatar = models.ImageField(upload_to='profile/',default='default/avatar.svg')
    shortBio = models.TextField(blank=True)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=60,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-createdAt']

class Skills(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=60, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.name
    

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    subject = models.CharField(max_length=60,null=True,blank=True)
    body = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-createdAt']
    
    


