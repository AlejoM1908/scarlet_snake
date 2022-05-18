from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from user.models import User
from user.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework import status, permissions

class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserRegistrationSerializer

    def get_list(self):
        users = User.objects.all()
        return users

    def get(self, request):
        
        user_id = request.query_params.get('id', None)
        if (user_id != None):
            user = User.objects.get(id=user_id)
            serializer = self.serializer_class(user)   
        else:
            user = self.get_list()
            serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)

    def put(self, request):
        user_id = request.query_params.get('id', None)
        user = User.objects.get(id= user_id)
        serializer = self.serializer_class(user, data= request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = request.query_params.get('id', None)
        user = get_object_or_404(User, id= user_id)
        user.delete()
        return Response(status= status.HTTP_202_ACCEPTED)

class UserRegistrationAPIView(GenericAPIView):
    authentication_classes = ()
    serializer_class = UserRegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(username=username, password=password)

        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Invalid authentication, try again'}, status=status.HTTP_401_UNAUTHORIZED)