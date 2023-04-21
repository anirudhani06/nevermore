from django.db import models
from account.models import Profile
from ckeditor.fields import RichTextField
import uuid
import math
# Create your models here.


class Projects(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    slug = models.SlugField(unique=True,null=True,blank=True)
    image = models.ImageField(upload_to='projects/')
    body = RichTextField()
    tags = models.ManyToManyField('Tag',blank=True)
    likes = models.ManyToManyField(Profile,blank=True,related_name='project_likes')
    dislikes = models.ManyToManyField(Profile,blank=True,related_name='project_dislikes')
    total_likes = models.IntegerField(default=0)
    feedback = models.IntegerField(default=0,blank=True)
    sourceCode = models.URLField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-createdAt']
    
    @property
    def positive_feedback(self):
        total_likes = self.likes.count() + self.dislikes.count()
        avg = (self.likes.count() / total_likes) * 100
        self.feedback = math.floor(avg)
        self.save()
    
class Tag(models.Model):
    name = models.CharField(max_length=60)
    createdAt = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)

    def __str__(self):
        return self.name


class Comments(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
    project = models.ForeignKey(Projects,on_delete=models.CASCADE)
    body = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)

    class Meta:
        ordering = ['-createdAt']
    
    def __str__(self):
        return self.body