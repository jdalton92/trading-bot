from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomAuthToken(ObtainAuthToken):
    """Create custom auth token."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'email': user.email,
            'token': token.key,
        },
            status=200
        )


class LoginView(APIView):
    """
    JSON login view.

    Sets session for successfully authenticated user.
    """

    permission_classes = []

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'user_id': user.pk,
                    'email': user.email,
                    'token': token.key,
                },
                status=200
            )
        else:
            return Response({"error": "User does not exist, or is inactive"}, status=400)
