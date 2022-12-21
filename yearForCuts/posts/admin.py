from django.contrib import admin

# Register your models here.
from .models import * # 모든 모델을 불러옵니다.

admin.site.register(Post)
admin.site.register(PostImage)