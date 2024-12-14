from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=50, allow_null=False, allow_blank=False)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=50, allow_null=False, allow_blank=False)
    
