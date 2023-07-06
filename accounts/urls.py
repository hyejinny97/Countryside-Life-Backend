from django.urls import path
from .views import ChangePasswordView, RegisterUserView, UserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='auth_register'),
    path('user/<int:pk>/', UserView.as_view(), name='auth_update_read_delete'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]
