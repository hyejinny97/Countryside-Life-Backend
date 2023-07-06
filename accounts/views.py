from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

# 회원가입
class RegisterUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterUserSerializer

# 조회/수정/탈퇴
class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

# 비밀번호 변경
class ChangePasswordView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated,]