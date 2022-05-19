from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from user.models import User
from django.conf import settings
import jwt


class JWTAuthentication(BaseAuthentication):
    """Used to decode a JSON Web Token and properly provide Oauth2 authorization in project"""

    def authenticate(self, request):
        """Used to process the given request to extract the JWT and decode it"""
        auth_header = get_authorization_header(request)
        token = auth_header.decode("utf-8").split(" ")

        # Token structure isn't 'Bearer $token'
        if len(token) != 2:
            raise exceptions.AuthenticationFailed("Invalid token provided")

        token = token[1]

        try:
            # Decoding the token with a secret key and extracting the User model info stored in it
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(username=payload["username"])

            return (user, token)

        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed("The provided token is expired")

        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed(
                "The provided token has invalid structure"
            )

        except User.DoesNotExist as e:
            raise exceptions.AuthenticationFailed("The token owner does not exists")
