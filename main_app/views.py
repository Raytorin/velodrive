from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.object.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]