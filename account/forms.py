from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm,PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Skills,Message

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','email','password1','password2')
        labels = {
            'first_name':'name',
        }

class SkillForm(ModelForm):
    class Meta:
        model = Skills
        fields = ('name','description')

class MessageForm(ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Subject'}))
    class Meta:
        model = Message
        fields = ('subject','body')

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ('new_password1','new_password2')


class PasswordResetForm(PasswordResetForm):
    def __init__(self,*args,**kwargs):
        super(PasswordResetForm,self).__init__(*args,**kwargs)
    