from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TEACHER = 1
    STUDENT = 2

    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student')
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    def __str__(self) -> str:
        return self.username