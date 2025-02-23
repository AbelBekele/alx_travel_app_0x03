from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Import AllowAny for public access
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow access without authentication
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(security=[])  # Disable authorization button for Swagger documentation
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(security=[])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)
