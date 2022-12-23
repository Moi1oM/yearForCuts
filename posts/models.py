# Create your models here.
from django.db import models
from accounts.models import User
from datetime import datetime
from django.utils import timezone
def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])

class BaseModel(models.Model):  # 수정시간, 생성시간 모델
    created_at = models.DateTimeField(default=datetime.now)  # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(auto_now=True)  # 해당 레코드 갱신시 현재 시간 자동저장

    class Meta:
        abstract = True  # 상속

# class Posts(models.Model):
#     creator = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="listings")
#     title = models.CharField(
#         max_length=80, blank=False, null=False)
#     letter = models.TextField()
#     image_url1 = models.ImageField(upload_to=nameFile, blank=True, null=True)
#     image_url2 = models.ImageField(upload_to=nameFile, blank=True, null=True)
#     image_url3 = models.ImageField(upload_to=nameFile, blank=True, null=True)
#     image_url4 = models.ImageField(upload_to=nameFile, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)


class Post(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(
        max_length=80, blank=False, null=False)
    letter = models.TextField()
#    board = models.ForeignKey(Board, on_delete=models.CASCADE)


    def __int__(self):
        return self.id

    class Meta:
        db_table = 'post'


# 이미지 업로드 경로
def image_upload_path(instance, filename):
    return f'{instance.post.id}/{filename}'


class PostImage(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'post_image'