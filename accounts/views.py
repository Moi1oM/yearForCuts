from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from django.core import serializers
import json
# from allauth.socialaccount.models import SocialAccount
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Create your views here.
# GOOGLE_CALLBACK_URI = str(os.environ.get("BASR_URL")) + 'accounts/google/callback/'


class ReturnNicknameView(APIView):
    @csrf_exempt
    def emailReturn(request):
        temp = json.loads(request.body)
        email = temp.get('email')
        user = User.objects.get(email=email)

        return JsonResponse({'nickname': str(user.nickname)})
    @csrf_exempt
    def pidReturn(request):
        temp = json.loads(request.body)
        pid = temp.get('pid')
        print(pid)
        user = User.objects.get(public_id = pid)
        # print(user)
        return JsonResponse({'email': str(user.email), 'hidden': user.hidden, 'nickname': str(user.nickname)})


class ChangeNicknameView(APIView):
    @csrf_exempt
    def changeNickname(request):
        if (request.method == 'POST'):
            temp = json.loads(request.body)
            email = temp.get('email')
            temp_user = User.objects.get(email=email)
            new_nickname = temp.get('nickname')
            print(new_nickname)
            if (new_nickname != None):
                update_user_nickname = User.objects.filter(email=email).update(nickname=new_nickname)
                return JsonResponse({'user': str(temp_user), 'pid':temp_user.public_id, 'status': '201 Updated'})
            else:
              return JsonResponse({ 'status': '300 Bad Request'})  
        return JsonResponse({'status': '500 Wrong Method'})

class ChangeHiddenView(APIView):
    @csrf_exempt
    def changeHidden(request):
        if (request.method == 'POST'):
            temp = json.loads(request.body)
            email = temp.get('email')
            temp_user = User.objects.get(email=email)
            
            if (temp_user.hidden == False):
                update_user_hidden = User.objects.filter(email=email).update(hidden=True)
                return JsonResponse({'user': str(temp_user), 'hiddenBefore':temp_user.hidden, 'hiddenAfter':True, 'status': '201 Updated'})
            if (temp_user.hidden == True):
                update_user_hidden = User.objects.filter(email=email).update(hidden=False)
                return JsonResponse({'user': str(temp_user), 'hiddenBefore':temp_user.hidden, 'hiddenAfter':False, 'status': '201 Updated'})
            else:
              return JsonResponse({ 'status': '300 Bad Request'})  
        return JsonResponse({'status': '500 Wrong Method'})




class GoogleAccountRegistrationView(APIView):
    @csrf_exempt
    def google_callback(request):
        BASE_URL = os.environ.get("BASE_URL")
        """
        Email Request
        """
        temp = json.loads(request.body)
        accessToken = temp.get('accessToken')
        print(accessToken)
        # refreshToken = request.data["refreshToken"]
        # idToken = request.data["idToken"]
        email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={accessToken}")
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return JsonResponse({'err_msg': 'failed to get email from google', 'status':'400 email failed'}, status=status.HTTP_400_BAD_REQUEST)
        email_req_json = email_req.json()
        email = email_req_json.get('email')
        print("?????????",email_req_status, email)
        """
        Signup or Signin Request
        """

        try:
            user = User.objects.get(email=email)

            serializedUser = UserSerializer(user)
            print('??????', user.nickname)
            # # ????????? ????????? ????????? Provider??? google??? ????????? ?????? ??????, ????????? ?????????
            # # ?????? SNS??? ????????? ??????
            # social_user = SocialAccount.objects.get(user=user)
            # if social_user is None:
            #     return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
            # if social_user.provider != 'google':
            #     return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
            # # ????????? Google??? ????????? ??????
            # data = {'access_token': accessToken}
            # accept = requests.post(
            #     f"{BASE_URL}accounts/accounts/google/login/finish/", data=data)
            # accept_status = accept.status_code
            # if accept_status != 200:
            #     return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
            # accept_json = accept.json()
            # accept_json.pop('user', None)
            return JsonResponse({'user': str(user), 'pid':user.public_id, 'nickname':user.nickname, 'status': '202 UserAlreadyExist' })

        except User.DoesNotExist:
            # ????????? ????????? ????????? ????????? ?????? ??????
            # data = {'access_token': accessToken}
            # print("?????????",data)
            new_user = User.objects.create_user( email, nickname=None, password=None)
            # return redirect("/login")
            return JsonResponse({'user': str(new_user), 'status': '201 Created'})
            # if serializer.is_valid():
            #     user = serializer.save()
                
            #     # jwt ?????? ??????
            #     token = TokenObtainPairSerializer.get_token(user)
            #     refresh_token = str(token)
            #     access_token = str(token.access_token)
            #     res = {
            #             "user": serializer.data,
            #             "message": "register successs",
            #             "google":{"access_token": accessToken},
            #             "token": {
            #                 "access": access_token,
            #                 "refresh": refresh_token,
            #             },
            #             "status": "200 OK",
            #         }

                
                # # jwt ?????? => ????????? ??????
                # res.set_cookie("access", access_token, httponly=True)
                # res.set_cookie("refresh", refresh_token, httponly=True)
                
                # return JsonResponse(res)
            # return JsonResponse({'status':"500 Internal Server Error"})
            # accept = requests.post(
            #     f"{BASE_URL}accounts/accounts/google/login/finish/", data=data)
            # accept_status = accept.status_code
            # if accept_status != 200:
            #     return JsonResponse({'err_msg': 'failed to signup', 'status': accept_status}, status=accept_status)
            # accept_json = accept.json()
            # accept_json.pop('user', None)
        ## return JsonResponse("registration")

class KakaoAccountRegistrationView(APIView):
    @csrf_exempt
    def kakao_callback(request):
        BASE_URL = os.environ.get("BASE_URL")
        """
        Email Request
        """
        temp = json.loads(request.body)
        accessToken = temp.get('accessToken')
        email = temp.get('email')
        print(email)
        # refreshToken = request.data["refreshToken"]
        # idToken = request.data["idToken"]
        # email_req = requests.get(
        # f"https://kapi.kakao.com/v2/user/me", headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8','Authorization': 'Bearer ' + accessToken})
        # email_req_status = email_req.status_code
        # print("?????????", email_req.json())
        # if email_req_status != 200:
        #     return JsonResponse({'err_msg': 'failed to get email from kakao', 'status':'400 email failed'}, status=status.HTTP_400_BAD_REQUEST)
        # email_req_json = email_req.json()
        # email = email_req_json.get('email')
        # print("?????????",email_req_status, email)
        """
        Signup or Signin Request
        """

        try:
            user = User.objects.get(email=email)

            serializedUser = UserSerializer(user)
            print('??????', user.nickname)
            return JsonResponse({'user': str(user), 'pid':user.public_id, 'nickname':user.nickname, 'status': '202 UserAlreadyExist' })

        except User.DoesNotExist:
            new_user = User.objects.create_user( email, nickname=None, password=None)
            # return redirect("/login")
            return JsonResponse({'user': str(new_user), 'status': '201 Created'})
