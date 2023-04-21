from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from base.models import Projects
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site

from .forms import RegisterForm,SkillForm,MessageForm,PasswordResetForm,SetPasswordForm
from .models import Skills,Profile,Message
from .decoraters import is_unauthenticate
from .tokens import account_activation_token
# Create your views here.

@is_unauthenticate
def validate_user(request,uidb64,token):
    User = get_user_model()

    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('link expired')
        
@is_unauthenticate
def vallidate_email(request,user,to_email):
    user = get_user_model().objects.filter(email=to_email).first()
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = account_activation_token.make_token(user)
    protocol = 'https' if request.is_secure() else 'http'

    url =f"{protocol}://{domain}/user/validate-email/{uidb64}/{token}"
    context = {'url':url}

    return render(request,'account/email_send_successfully.html',context)

@csrf_exempt
@is_unauthenticate
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Credantials!')

    return render(request,'account/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')

@csrf_exempt
@is_unauthenticate
def user_register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active = False
            user.save()

            return vallidate_email(request,user,form.cleaned_data['email'])

    context = {'form':form}
    return render(request,'account/register.html',context)

@method_decorator(login_required(login_url='login'),name='dispatch')
class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

@is_unauthenticate
def forget_password(request):
    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            assosiated_user = get_user_model().objects.filter(Q(email=user_email)).first()

            if assosiated_user:            
                domain = get_current_site(request).domain
                uid = urlsafe_base64_encode(force_bytes(assosiated_user.id))
                token = account_activation_token.make_token(assosiated_user)
                protocol = 'https' if request.is_secure() else 'http'
                
                url = f"{protocol}://{domain}/user/reset-password/{uid}/{token}"
                context = {'url':url}

                return render(request,'account/email_send_successfully.html',context)

    context = {'form':form}
    return render(request,'account/forget_password.html',context)

    

def password_reset_confirm(request,uidb64,token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None



    
    
    if user is not None and account_activation_token.check_token(user,token):
        form = SetPasswordForm(user)
        if request.method == "POST":
            form = SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()

                return redirect('login')
        context = {'form':form}
        return render(request,'account/password_reset_confirm.html',context)
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    
        
       
    


@login_required(login_url='login')
def my_account(request):
    skills = Skills.objects.filter(owner=request.user.profile)
    projects = Projects.objects.filter(owner=request.user.profile)
    context = {'skills':skills,'projects':projects}
    return render(request,'account/my_account.html',context)

@login_required(login_url='login')
@csrf_exempt
def update_profile(request):

    profile = request.user.profile

    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        domain = request.POST.get('domain')
        location = request.POST.get('location')
        email = request.POST.get('email')
        shortBio = request.POST.get('shortBio')
        about = request.POST.get('about')

        try:
            profile.avatar = request.FILES['avatar']
        except:
            profile.avatar = profile.avatar

        profile.name = name
        profile.username = username
        profile.domain = domain
        profile.location = location
        profile.email = email
        profile.shortBio = shortBio
        profile.about = about
        profile.save()
        return redirect('my-account')

    context = {'profile':profile}
    return render(request,'account/update_profile.html',context)


@login_required(login_url='login')
@csrf_exempt
def add_skills(request):
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            return redirect('my-account')
        
    context = {'form':form}
    return render(request,'account/skill.html',context)

@login_required(login_url='login')
@csrf_exempt
def update_skills(request,skill_id):
    skill = Skills.objects.get(id=skill_id)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)

        if form.is_valid():
            form.save()

            return redirect('my-account')
        
    context = {'form':form}
    return render(request,'account/skill.html',context)

@login_required(login_url='login')
@csrf_exempt
def delete_skill(request):
    if request.method == "POST":
        skill_id = request.POST.get('id')
        skill = Skills.objects.get(id=skill_id)

        if skill.owner == request.user.profile:
            skill.delete()
        else:
            return HttpResponse('You cant delete!')

        return redirect('my-account')

@login_required(login_url='login')
def profile(request,username):
    user = Profile.objects.get(username=username)
    if user == request.user.profile:
        return redirect('my-account')
    
    projects = Projects.objects.filter(owner = user)
    context = {'user':user,'projects':projects}
    return render(request,'account/profile.html',context)

@login_required(login_url='login')
@csrf_exempt
def send_message(request,username):
    receiver = Profile.objects.get(username=username)
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.recipient = receiver
            message.save()

            return HttpResponseRedirect(f"/user/profile/{username}")

    context = {'receiver':receiver,'form':form}
    return render(request,'account/send_message.html',context)

@login_required(login_url='login')
def inbox(request):
    messages = Message.objects.filter(recipient=request.user.profile)
    msg_count = messages.count()
    new_messages_count = messages.filter(is_read=False).count()
    context = {'messages':messages,'msg_count':msg_count,'new_messages_count':new_messages_count}
    return render(request,'account/inbox.html',context)

@login_required(login_url='login')
def message(request,message_id):
    message = Message.objects.get(id=message_id)
    message.is_read = True
    message.save()
    context = {'message':message}
    return render(request,'account/message.html',context)

@login_required(login_url='login')
def delete_my_account(request,user_id):
    if str(request.user.profile.id) != user_id:
        return HttpResponse("You can't delete this account!")
    
    user = Profile.objects.filter(id=user_id).first()
    user.delete()

   
    return redirect('home')
