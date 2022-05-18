from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from course.models import Course
from course.serializers import CourseSerializer
from rest_framework import status, permissions

class CourseAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CourseSerializer
    
    def get_list(self, user):
        courses = Course.objects.filter(us_id= user)
        return courses

    def post(self, request):
        serializer = self.serializer_class(data= request.data)

        if serializer.is_valid():
            serializer.save(us_id = [self.request.user])
            return Response(serializer.data, status= status.HTTP_201_CREATED)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        
        course_id = request.query_params.get('id', None)
        if (course_id != None):
            course = Course.objects.get(id=course_id)
            serializer = CourseSerializer(course)   
        else:
            course = self.get_list(self.request.user)
            serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)

    def put(self, request):
        course_id = request.query_params.get('id', None)
        course = Course.objects.get(id= course_id)
        serializer = self.serializer_class(course, data= request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        course_id = request.query_params.get('id', None)
        couse = get_object_or_404(Course, id= course_id)
        couse.delete()
        return Response(status= status.HTTP_202_ACCEPTED)
