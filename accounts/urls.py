from allauth.account.views import confirm_email
from django.contrib import admin
from django.urls import path, include, re_path
from accounts import views

urlpatterns = [
    re_path(r'^rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    path('google/callback/', views.GoogleAccountRegistrationView.google_callback,name='google_callback'), 
    path('nickname/', views.ReturnNicknameView.emailReturn ,name='emailReturn'), 
    path('nickname/pid', views.ReturnNicknameView.pidReturn ,name='pidReturn'), 
    path('nickname/change', views.ChangeNicknameView.changeNickname ,name='changeNickname'), 
]