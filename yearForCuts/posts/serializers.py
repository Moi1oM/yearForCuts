from rest_framework import serializers
from .models import Post, PostImage
from accounts.models import User
# from .models import MyModel

# class PostSerializer(serializers.ModelSerializer):
#     # creator = serializers.ReadOnlyField(source='creator.email')
#     # creator_id = serializers.ReadOnlyField(source='creator.id')
#     # image_url1 = serializers.ImageField(required=False)
#     # image_url2 = serializers.ImageField(required=False)
#     # image_url3 = serializers.ImageField(required=False)
#     # image_url4 = serializers.ImageField(required=False)
#     class Meta:
#         model = Post
#         fields = '__all__'



class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostImage
        fields = ['image']


class PostSerializer(serializers.ModelSerializer):
    
    images = serializers.SerializerMethodField()

	#게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        image = obj.image.all() 
        return PostImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        print("testing data", validated_data)
        instance = Post.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            PostImage.objects.create(post=instance, image=image_data)
        return instance