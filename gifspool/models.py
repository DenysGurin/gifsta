from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'gifspool/{0}/{1}'.format(instance.creator.id, filename)

class Category(models.Model):
	name = models.CharField(max_length=30)
	num_gifs = models.IntegerField()
	num_likes = models.IntegerField()

class Gif(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True,
    null=True,)
	creator = models.ForeignKey(User, default='')
	name = models.CharField(max_length=30)
	tags = models.CharField(max_length=300)
	upload_date = models.DateTimeField(auto_now_add=True)
	likes_by = models.TextField(default='', blank = True)
	likes = models.IntegerField(default=0)
	shocked = models.IntegerField(default=0)
	loved = models.IntegerField(default=0)
	laugh = models.IntegerField(default=0)
	post_to = models.BooleanField(default=False)
	gif_file = models.FileField(upload_to=user_directory_path)

class Like(models.Model):
	gif_id = models.ForeignKey(Gif, on_delete=models.CASCADE, blank=True,
    null=True,)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
    null=True,)
	shocked = models.BooleanField(default=False)
	loved = models.BooleanField(default=False)
	laugh = models.BooleanField(default=False)
