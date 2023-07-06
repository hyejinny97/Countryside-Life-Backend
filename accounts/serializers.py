from rest_framework import serializers
from .models import User
from django.contrib.auth import password_validation
import django.contrib.auth.password_validation as validators

# 회원가입
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'nickname')

    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user


# 조회/수정/탈퇴
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'nickname']
    
    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.nickname = validated_data['nickname']
        instance.save()

        return instance

# 비밀번호 변경
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return data
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance