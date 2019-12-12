from django.db import models

# Create your models here.

from django.contrib.auth.models import User   

class UserPicture(models.Model):
        user = models.OneToOneField(User, on_delete = models.CASCADE)
        picture = models.ImageField(upload_to='media')
