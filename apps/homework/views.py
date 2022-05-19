from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from homework.models import Homework, Submition
from homework.serializers import HomeworkSerializer, SubmitionSerializer
from rest_framework import status, permissions
from helpers.upload import Upload


class HomeworkAPIView(GenericAPIView):
    """Used to generate some token protected endpoints for homeworks info"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = HomeworkSerializer

    def get_list(self, user):
        """Used to get all the stored homeworks basic info"""
        homeworks = Homework.objects.filter(us_id=user)
        return homeworks

    def post(self, request):
        """Used to create a new homework"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(us_id=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Used to get the homework with the given id or all the homeworks if id not provided"""
        homework_id = request.query_params.get("id", None)
        if homework_id != None:
            homework = Homework.objects.get(id=homework_id)
            serializer = self.serializer_class(homework)
        else:
            homework = self.get_list(self.request.user)
            serializer = self.serializer_class(homework, many=True)
        return Response(serializer.data)

    def put(self, request):
        """Used to update the homework info"""
        homework_id = request.query_params.get("id", None)
        homework = Homework.objects.get(id=homework_id)
        serializer = self.serializer_class(homework, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Used to delete a homework"""
        homework_id = request.query_params.get("id", None)
        homework = get_object_or_404(Homework, id=homework_id)
        homework.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class SubmitionAPIView(GenericAPIView):
    """Used to generate some token protected endpoints for submitions info"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubmitionSerializer

    def get_list(self, user):
        """Used to get all the stored submitions basic info"""
        submitions = Submition.objects.filter(us_id=user)
        return submitions

    def post(self, request):
        """Used to create a new submition"""
        data_url = Upload.upload_file(request.data["data"], request.data["data"].name)
        request.data["data"] = data_url
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(us_id=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Used to get the submition with the given id or all the submitions if id not provided"""
        submition_id = request.query_params.get("id", None)
        if submition_id != None:
            submition = Submition.objects.get(id=submition_id)
            serializer = self.serializer_class(submition)
        else:
            submition = self.get_list(self.request.user)
            serializer = self.serializer_class(submition, many=True)
        return Response(serializer.data)

    def put(self, request):
        """Used to update the submition info"""
        submition_id = request.query_params.get("id", None)
        submition = Submition.objects.get(id=submition_id)
        serializer = self.serializer_class(submition, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Used to delete a submition"""
        submition_id = request.query_params.get("id", None)
        submition = get_object_or_404(Submition, id=submition_id)
        submition.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
