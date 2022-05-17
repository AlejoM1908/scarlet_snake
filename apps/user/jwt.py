from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from user.models import User
from django.conf import settings
import jwt

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        token = auth_header.decode('utf-8').split(' ')

        if len(token) != 2:
            raise exceptions.AuthenticationFailed('Invalid token provided')

        token = token[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(username= payload['username'])

            return (user, token)

        except jwt.ExpiredSignatureError as excep:
            raise exceptions.AuthenticationFailed('The provided token is expired')

        except jwt.DecodeError as excep:
            raise exceptions.AuthenticationFailed('The provided token has invalid structure')

        except User.DoesNotExist as excep:
            raise exceptions.AuthenticationFailed('The token owner does not exists')