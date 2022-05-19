from django.db import models
from user.models import User
from helpers.models import TrackingModel


class Course(TrackingModel):
    """Model to manage the courses info in the database and requests"""

    readonly_fields = ("id",)
    us_id = models.ManyToManyField(User)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name
