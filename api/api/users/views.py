
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        return User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the user view
        requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
