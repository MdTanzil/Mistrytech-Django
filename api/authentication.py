from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework import  permissions
class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            return user  # Return the user if found
        except UserModel.DoesNotExist:
            return None  # User does not exist


class PostRequestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow POST requests for unauthenticated users
        if request.method == 'POST' and not request.user.is_authenticated:
            return True
        # Allow other requests for authenticated users
        return request.user and request.user.is_authenticated