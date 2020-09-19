from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    pwd = models.CharField(max_length=30)