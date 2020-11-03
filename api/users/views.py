from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer


class UserView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return UserSerializer
