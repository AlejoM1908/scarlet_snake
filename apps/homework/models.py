from django.db import models
from user.models import User
from course.models import Course
from helpers.models import TrackingModel


class Homework(TrackingModel):
    """Model to manage the homeworks info in the database and requests"""

    us_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cs_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    limit_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Submition(models.Model):
    """Model to manage the submitions info in the database and requests"""

    us_id = models.ForeignKey(User, on_delete=models.CASCADE)
    hw_id = models.ForeignKey(Homework, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    data = models.TextField(max_length=1500, unique=True)

    def __str__(self) -> str:
        return f"submit date: {self.created_at}"
