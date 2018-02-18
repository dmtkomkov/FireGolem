from django.db import models
from django.contrib.auth.models import User


class UserIcon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon = models.CharField(max_length=100)
