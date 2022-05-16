from django.db import models
from user.models import User
from course.models import Course

class Homework(models.Model):
    us_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cs_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    creation_date = models.DateTimeField()
    limit_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Submition(models.Model):
    us_id = models.ForeignKey(User, on_delete=models.CASCADE)
    hw_id = models.ForeignKey(Homework, on_delete=models.CASCADE)
    submit_date = models.DateTimeField()
    score = models.IntegerField()
    data = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'submit date: {self.submit_date}'