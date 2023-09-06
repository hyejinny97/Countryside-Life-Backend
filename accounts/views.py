from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models.query import prefetch_related_objects
from .serializers import RegisterUserSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# 회원가입
class RegisterUserView(generics.CreateAPIView):
    print('겟 유저모델', get_user_model())
    queryset = get_user_model().objects.all()
    serializer_class = RegisterUserSerializer


# 조회/수정/탈퇴
class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def extract_user_id_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get('user_id')
            return user_id
        except Exception as e:
            return None

    def retrieve(self, request, *args, **kwargs):
        # instance = self.get_object() 
        instance = get_user_model().objects.get(id=self.extract_user_id_from_token(str(request.auth)))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        instance = get_user_model().objects.get(id=self.extract_user_id_from_token(str(request.auth)))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance,
            # and then re-prefetch related objects
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # instance = self.get_object()
        instance = get_user_model().objects.get(id=self.extract_user_id_from_token(str(request.auth)))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


# 비밀번호 변경
class ChangePasswordView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated,]

    def extract_user_id_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get('user_id')
            return user_id
        except Exception as e:
            return None
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        instance = get_user_model().objects.get(id=self.extract_user_id_from_token(str(request.auth)))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    

# 로그아웃
class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")