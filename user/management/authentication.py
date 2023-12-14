from datetime import datetime, timedelta

import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from user.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user from the database
        name_or_contact_number = payload.get('user_identifier')
        if name_or_contact_number is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(name=name_or_contact_number).first()
        if user is None:
            user = User.objects.filter(contact_number=name_or_contact_number).first()
            if user is None:
                raise AuthenticationFailed('User not found')

        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):
        # Create the JWT payload
        payload = {
            'user_identifier': user.name,
            'exp': int((datetime.now() + timedelta(hours=settings.SIMPLE_JWT['TOKEN_LIFETIME_HOURS'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'username': user.name,
            'contact_number': user.contact_number
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token
