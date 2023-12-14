from rest_framework import generics, status, permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.api.serializers import RegisterSerializer, UpdateUserSerializer, \
    ObtainTokenSerializer
from user.management.authentication import JWTAuthentication
from user.models import User


class RegisterUserAPIView(ListAPIView, CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class ObtainTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
        password = serializer.validated_data.get('password')
        user = User.objects.filter(name=name).first()
        if user is None:
            user = User.objects.filter(contact_number=name).first()

        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        return Response({'token': jwt_token})


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
