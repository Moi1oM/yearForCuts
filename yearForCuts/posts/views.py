import json
from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework import status
# Create your views here.
from .models import Post, PostImage
from .serializers import PostSerializer
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
import os
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from posts import views
from accounts.models import User
from django.core import serializers

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes=[permissions.AllowAny, ]

@csrf_exempt
def checking_google(request):
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
        return JsonResponse({'err_msg': 'failed to get email'},status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    print("이메일",email_req_status, email)
    hi_user = User.objects.get(email=email)
    userPosts = Post.objects.filter(creator=hi_user.pk)
    postdatas = list(userPosts.values())
    #print(postdatas)
    d=[]
    for i in postdatas:
        #print("start from this",i)
        newdict = {}
        newdict['title']=i['title']
        newdict['letter']=i['letter']
        tmp=PostImage.objects.filter(post=i.get('id'))
        userPostImg = serializers.serialize("json", tmp)
        userPostImg = json.loads(userPostImg)
        #print("how can i use this",userPostImg, type(userPostImg))
        idx=1
        plusdict={}
        for j in userPostImg:
            #print("this is loop",j, type(j))
            plusdict[f'image{idx}']=j['fields'].get('image')
            idx+=1
        #print("this is plusdict",plusdict)
        newdict['images']=plusdict
        d.append(newdict)
    #print("this is d ",d)
    return JsonResponse({'posts': d})



# class PostCreateView(APIView):
#     @csrf_exempt
#     def checking_google(request):
#         BASE_URL = os.environ.get("BASE_URL")
#         """
#         Email Request
#         """
#         temp = json.loads(request.body)
#         accessToken = temp.get('accessToken')
#         # refreshToken = request.data["refreshToken"]
#         # idToken = request.data["idToken"]
#         email_req = requests.get(
#         f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={accessToken}")
#         email_req_status = email_req.status_code

#         if email_req_status != 200:
#             return JsonResponse({'err_msg': 'failed to get email'},status=status.HTTP_400_BAD_REQUEST)
#         email_req_json = email_req.json()
#         email = email_req_json.get('email')
#         print("이메일",email_req_status, email)
#         if request.method == 'POST':
#             new_post = Post.objects.create(email, )

@api_view(['GET', 'POST'])
@csrf_exempt
def post_list(request):

    if request.method == 'GET':
        posts = Post.objects.filter(creator=email)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'status':'status.HTTP_404_NOT_FOUND'})

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PostViewSet(ModelViewSet):
#     queryset = Post.objects.all().order_by('-created_at')
#     serializer_class = PostSerializer
#     filter_backends = [DjangoFilterBackend]

# class ImageViewSet(ListAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostSerializer
#     def get_posts(request):
#         BASE_URL = os.environ.get("BASE_URL")
#         """
#         Email Request
#         """
#         temp = json.loads(request.body)
#         accessToken = temp.get('accessToken')
#         # refreshToken = request.data["refreshToken"]
#         # idToken = request.data["idToken"]
#         email_req = requests.get(
#         f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={accessToken}")
#         email_req_status = email_req.status_code

#         if email_req_status != 200:
#             return JsonResponse({'err_msg': 'failed to get email'},status=status.HTTP_400_BAD_REQUEST)
#         email_req_json = email_req.json()
#         email = email_req_json.get('email')
#         print("이메일",email_req_status, email)


#     def post(self, request, *args, **kwargs):
#         file = request.data['file']
#         image = Posts.objects.create(image=file)
#         return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)