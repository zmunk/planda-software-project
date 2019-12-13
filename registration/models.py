from django.db import models

# Create your models here.

from django.contrib.auth.models import User   

class UserProfile(models.Model):
    user = models.OneToOneField(User,unique=True, on_delete = models.CASCADE)
    picture = models.ImageField(default = 'default.png', upload_to='')

