import os
import redis
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache

from PIL import Image
import moviepy.editor as mp

from .make_media import gif_to_jpg, gif_to_mp4


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'gifspool/{0}/{1}'.format(instance.creator.id, filename)

class Category(models.Model):
    name = models.CharField(max_length=30, default="", blank = True)
    site_name = models.CharField(max_length=30, default="", blank = True)
    num_gifs = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)
    post_to = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=60, unique = True)
    count = models.IntegerField(default=1)
    def __str__(self):
        return self.hashtag


class Gif(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,)
    creator = models.ForeignKey(User, default='')
    name = models.CharField(max_length=30)
    tags = models.CharField(max_length=300, blank = True)
    upload_date = models.DateTimeField(auto_now_add=True, blank = True)
    likes_by = models.TextField(default='', blank = True)
    likes = models.IntegerField(default=0)
    shocked = models.IntegerField(default=0)
    loved = models.IntegerField(default=0)
    laugh = models.IntegerField(default=0)
    post_to = models.BooleanField(default=None)
    gif_file = models.FileField(upload_to=user_directory_path)

    mp4_file_url = models.CharField(max_length=60, null=True, blank = True)
    jpg_path = models.CharField(max_length=60, default="", null=True, blank = True)
    jpg_url = models.CharField(max_length=60, default="", null=True, blank = True)

    views = models.IntegerField(default=0, blank=True, null=True,)

    hashtags = models.ManyToManyField(Hashtag, through='GifHashtagLinker', related_name = 'gifs_hashtag', blank=True )
    liked_by = models.ManyToManyField(User, through='Like', related_name = 'liked_by_user', blank=True)

    prev_gif = models.IntegerField(default=None, null=True, blank = True)
    next_gif = models.IntegerField(default=None, null=True, blank = True)

    def save(self, *args, **kwargs):

        super(Gif, self).save(*args, **kwargs)
        path = self.gif_file.path
        file_url = self.gif_file.url
        new_path = os.path.splitext(path)[0]
        new_file_url = os.path.splitext(file_url)[0]

        # try:
        self.prev_gif = self.pk-1#Gif.objects.get(pk=int(pk)-1)
        self.next_gif = self.pk+1
        # except:
        #     pass
        try:
            cache.set('to_update', True)
        except redis.exceptions.ConnectionError:
            pass
        if os.path.splitext(path)[1] == ".gif":
            
            

            if not os.path.isfile('%s.jpg'%new_path):
                gif_to_jpg(path, new_path)
                self.jpg_path = "%s.jpg"%new_path
                self.jpg_url = "%s.jpg"%new_file_url
        elif os.path.splitext(path)[1] == ".jpg":
            self.jpg_path = self.gif_file.path
            self.jpg_url = self.gif_file.url

        if not os.path.isfile('%s.mp4'%new_path):
            gif_to_mp4(path, new_path)
            self.mp4_file_url = self.gif_file.url.replace(".gif", ".mp4")

    def __str__(self):
        return "%s-%s "%(str(self.id), self.name)


class GifView(models.Model):
    gif = models.ForeignKey(Gif, on_delete=models.CASCADE, blank=True, null=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    ip_address = models.CharField(max_length=30)
    view_date = models.DateTimeField(auto_now_add=True, null=True, blank = True)

    def __str__(self):
        return "%s "%str(self.id)


class Like(models.Model):
    gif_id = models.ForeignKey(Gif, on_delete=models.CASCADE, blank=True, null=True,)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    shocked = models.BooleanField(default=False)
    loved = models.BooleanField(default=False)
    laugh = models.BooleanField(default=False)
    like_date = models.DateTimeField(auto_now_add=True, null=True, blank = True)

    def __str__(self):
        return "%s "%str(self.id)


class GifHashtagLinker(models.Model):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, blank=True, null=True,)
    gif = models.ForeignKey(Gif, on_delete=models.CASCADE, blank=True, null=True,)

    def __str__(self):
        return "%s "%str(self.id)

