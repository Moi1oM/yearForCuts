from rest_framework import serializers

# from accounts.models import CustomUser, User
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # model = CustomUser
        fields = ['email', 'nickname', 'password']
        
        
        
class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # model = CustomUser
        fields = ['email', 'nickname']
    def create(self, validated_data):
        # user = CustomUser.objects.create_user(
        user = User.objects.create_user(
            validated_data["email"], None
        )
        return user