from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('validate-email/<uidb64>/<token>',views.validate_user,name='validate-email'),
    path('logout/',views.user_logout,name='logout'),

    path('my-account',views.my_account,name='my-account'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),

    path('add-skill',views.add_skills,name='add-skill'),
    path('update-skill/<str:skill_id>',views.update_skills,name='update-skill'),
    path('delete-skill',views.delete_skill,name='delete-skill'),

    path('inbox',views.inbox,name='inbox'),
    path('message/<str:message_id>',views.message,name='message'),
    path('send-message/<str:username>',views.send_message,name='send-message'),

    path('change-password',views.PasswordChangeView.as_view(template_name="account/change_password.html"),name='change-password'),
    path('forget-password',views.forget_password,name='forget-password'),
    path('reset-password/<uidb64>/<token>',views.password_reset_confirm,name='reset-password'),

    path('delete-my-account/<str:user_id>',views.delete_my_account,name='delete-my-account'),
    
]
