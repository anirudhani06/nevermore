from django.forms import ModelForm
from .models import Projects,Comments
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = ('image','title','sourceCode','tags','body')

class CommentForm(ModelForm):
     class Meta:
        model = Comments
        fields = ('body',)