from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from user.models import User
from user.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework import status, permissions


class AuthUserAPIView(GenericAPIView):
    """Used to generate some token protected endpoints for users info"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserRegistrationSerializer

    def get_list(self):
        """Used to get all the stored users basic info"""
        users = User.objects.all()
        return users

    def get(self, request):
        """Used to get the user with the given id or all the users if id not provided"""
        user_id = request.query_params.get("id", None)
        if user_id != None:
            user = User.objects.get(id=user_id)
            serializer = self.serializer_class(user)
        else:
            user = self.get_list()
            serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)

    def put(self, request):
        """Used to update the user info"""
        user_id = request.query_params.get("id", None)
        user = User.objects.get(id=user_id)
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Used to delete a user"""
        user_id = request.query_params.get("id", None)
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class UserRegistrationAPIView(GenericAPIView):
    """Used to generate public endpoints for new users registration"""

    authentication_classes = ()
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        """Used to create a new user"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(GenericAPIView):
    """Used to generate a public endpoint for user login and JWT token generation"""

    authentication_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = authenticate(username=username, password=password)

        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "Invalid authentication, try again"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
