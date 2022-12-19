from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework import status
from accounts.models import User
# from accounts.models import CustomUser, User
import json
from allauth.socialaccount.models import SocialAccount
import os
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
# GOOGLE_CALLBACK_URI = str(os.environ.get("BASR_URL")) + 'accounts/google/callback/'
@csrf_exempt
def google_callback(request):
    BASE_URL = os.environ.get("BASE_URL")
    """
    Email Request
    """
    temp = json.loads(request.body)
    # print("이거임", BASE_URL)
    accessToken = temp.get('accessToken')
    # refreshToken = request.data["refreshToken"]
    # idToken = request.data["idToken"]
    email_req = requests.get(
    f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={accessToken}")
    email_req_status = email_req.status_code

    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'},status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    print("이메일",email_req_status, email)
    """
    Signup or Signin Request
    """

    try:
        user = User.objects.get(email=email)
        # user = CustomUser.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # # 기존에 Google로 가입된 유저
        # data = {'access_token': accessToken}
        # accept = requests.post(
        #     f"{BASE_URL}accounts/accounts/google/login/finish/", data=data)
        # accept_status = accept.status_code
        # if accept_status != 200:
        #     return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        # accept_json = accept.json()
        # accept_json.pop('user', None)
        return JsonResponse(user)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': accessToken}
        print("데이타",data)
        
        
        # accept = requests.post(
        #     f"{BASE_URL}accounts/accounts/google/login/finish/", data=data)
        # accept_status = accept.status_code
        # if accept_status != 200:
        #     return JsonResponse({'err_msg': 'failed to signup', 'status': accept_status}, status=accept_status)
        # accept_json = accept.json()
        # accept_json.pop('user', None)
        return JsonResponse("registration")