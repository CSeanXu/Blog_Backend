from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView

from users.models import UserProfile
from users.api.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterView(CreateAPIView):
    """
    User Register
    """
    model = UserProfile
    serializer_class = UserRegisterSerializer


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    @method_decorator(csrf_exempt)
    def post(self, request):
        """User login with username and password."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
