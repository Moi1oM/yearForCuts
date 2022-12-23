
from django.contrib import admin
# from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts import views
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    #path('',include(router.urls)),
    path('newPost',views.new_Post),
    path('givePosts',views.checking_google),
    path('getUserPk',views.checkUserPk),
]
    # path('post_list/',views.post_list, name='post_list'),
    # path('post_detail/<int:pk>/',views.post_detail, name="post_detail"),


# urlpatterns = [    
#     path('upload/', views.ImageViewSet.as_view(), name='upload'),
# ]