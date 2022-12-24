import json
from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework import status
# Create your views here.
from .models import Post, PostImage, Color
from accounts.models import User
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
import uuid
import boto3

# class PostViewSet(ModelViewSet):
#     queryset = Post.objects.all().order_by('-created_at')
#     serializer_class = PostSerializer
#     filter_backends = [DjangoFilterBackend]
#     permission_classes=[permissions.AllowAny, ]


def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


@csrf_exempt
def new_Post(request):
    if (request.method == 'POST'):
        try:
            post = Post()
            post.title = request.POST['title']
            post.letter = request.POST['letter']
            post.color = request.POST['color']
            post.frame = int(request.POST['frame'])
            # post.pub_date = timezone.datetime.now()
            pid = request.POST['public_id']
            # print("this is pid", pid, type(pid))
            # uuid_string = uuid.UUID(pid).hex
            # print (is_valid_uuid(pid))
            # print(uuid.UUID(pid))
            # print("this is uuid string",uuid_string, type(uuid_string))
            user = User.objects.get(public_id=pid)
            print("this is user", user)
            post.user = user
            post.save()
            # name 속성이 imgs인 input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다
            print(request.FILES.getlist('image'))
            for img in request.FILES.getlist('image'):
                # Photo 객체를 하나 생성한다.
                photo = PostImage()
                # 외래키로 현재 생성한 Post의 기본키를 참조한다.
                photo.post = post
                # imgs로부터 가져온 이미지 파일 하나를 저장한다.
                photo.image = img
                # 데이터베이스에 저장
                print("here?")
                photo.save()
                print("here2?")
            return JsonResponse({'status': '200 created!', 'post_pk': post.pk, 'user_email': user.email})
        except Exception:
            print(Exception)
            return JsonResponse({'status': 'something wrong.. i`m sorry.'})


@csrf_exempt
def checkUserPk(request):
    temp = json.loads(request.body)
    email = temp.get('email')
    user = User.objects.get(email=email)
    print(user)
    return JsonResponse({'status': '200', 'userPk': str(user.pk)})


@csrf_exempt
def checking_google(request):
    BASE_URL = os.environ.get("BASE_URL")
    temp = json.loads(request.body)
    publicId = temp.get('pid')
    # refreshToken = request.data["refreshToken"]
    # idToken = request.data["idToken"]
    hi_user = User.objects.get(public_id=publicId)
    userPosts = Post.objects.filter(user=hi_user.pk)
    # print("userPosts",userPosts)
    postdatas = list(userPosts.values())
    # print("postsdatas",postdatas)
    d = []
    print("posts", postdatas)
    for i in postdatas:
        # print("start from this",i)
        newdict = {}
        newdict['post_pk'] = i['id']
        newdict['title'] = i['title']
        newdict['letter'] = i['letter']
        newdict['color'] = i['color']
        newdict['frame'] = i['frame']
        tmp = PostImage.objects.filter(post=i.get('id'))
        userPostImg = serializers.serialize("json", tmp)
        userPostImg = json.loads(userPostImg)
        # print("how can i use this",userPostImg, type(userPostImg))
        idx = 1
        plusdict = {}
        for j in userPostImg:
            # print("this is loop",j, type(j))
            plusdict[f'image{idx}'] = j['fields'].get('image')
            idx += 1
        # print("this is plusdict",plusdict)
        newdict['images'] = plusdict
        d.append(newdict)
        # print("newdict",newdict)
    # print("this is d ",d)
    return JsonResponse({'posts': d})


@csrf_exempt
def deletePost(request):
    try:
        temp = json.loads(request.body)
        post_pk = temp.get('post_pk')
        deleting_post = Post.objects.get(id=post_pk)
        deleting_images = PostImage.objects.filter(post=deleting_post.pk)
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        )
        userPostImg = serializers.serialize("json", deleting_images)
        userPostImg = json.loads(userPostImg)
        print("userPostImg", userPostImg)
        for i in userPostImg:
            pk = i['pk']
            key = i['fields'].get('image')
            print("image-name", key)
            print("pk", pk)
            s3_client.delete_object(Bucket=os.environ.get(
                'AWS_STORAGE_BUCKET_NAME'), Key=key)
            singleImage = PostImage.objects.get(id=pk)
            singleImage.delete()
        deleting_post.delete()
        return JsonResponse({'status': '200 success!'})
    except Exception:
        return JsonResponse({'status': '500'})


def ReturnColor(request):
    colorlist = Color.objects.all()
    temp = []
    for i in colorlist:
        temp.append(i.code)

    print(temp)
    # serializer = PostSerializer(posts, many=True)
    return JsonResponse({'colorlist': temp})

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
        return JsonResponse({'status': 'status.HTTP_404_NOT_FOUND'})

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
