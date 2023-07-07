from django.urls import path
from .views import ChangePasswordView, RegisterUserView, UserView, BlacklistRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='auth_register'),
    path('user/', UserView.as_view(), name='auth_update_read_delete'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', BlacklistRefreshView.as_view(), name="logout"),
]
