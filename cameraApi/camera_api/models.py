import os
from sysconfig import get_path
from django.db import models

def get_frame_path(instance, filename):
    """ creates unique-Path & filename for upload """

    path = os.path.join(instance.path, filename)
    return path


# Create your models here.
class Data(models.Model):
    path = models.CharField(max_length=100)
    frame = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=False)
    position = models.CharField(max_length= 50)
    name = models.CharField(max_length= 50)

class Video(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    time_interval = models.CharField(max_length=100)