from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from user.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework import status, permissions

class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserRegistrationSerializer(user)

        return Response({'user': serializer.data})

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