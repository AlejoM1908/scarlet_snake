from django.db import models
from user.models import User

class Course(models.Model):
    us_id = models.ManyToManyField(User)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name