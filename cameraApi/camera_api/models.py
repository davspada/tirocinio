import os
from sysconfig import get_path
from django.db import models

def get_frame_path(instance, filename):
    """ creates unique-Path & filename for upload """
    #ext = filename#.split('.')[-1]
    #filename = "%s%s.%s" % ( ext)

    path = os.path.join(instance.path, filename)
    #print(path)
    #os.makedirs(path, exist_ok=True)
    return path


# Create your models here.
class Data(models.Model):
    path = models.CharField(max_length=100)
    frame = models.ImageField(upload_to=get_frame_path)  #upload_to specifies the directory the images are going to reside
    timestamp = models.DateTimeField(auto_now=False)
    position = models.CharField(max_length= 50)
    name = models.CharField(max_length= 50)
