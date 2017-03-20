from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'gifspool/{0}/{1}'.format(instance.creator, filename)


class Gif(models.Model):
	creator = models.CharField(max_length=30, default='')
	name = models.CharField(max_length=30)
	tags = models.CharField(max_length=300)
	upload_date = models.DateTimeField(auto_now_add=True)
	likes = models.TextField(default='')	
	post_to = models.BooleanField(default=False)
	gif_file = models.FileField(upload_to=user_directory_path)
	gif_path = models.FilePathField(path=user_directory_path, default='')
