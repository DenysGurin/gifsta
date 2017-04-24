from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.conf import settings
from django.http import HttpResponse
from celery.task.schedules import crontab
# from .views import gifs_queue
from .models import Gif
from datetime import timedelta
from gifsta.celery import app

from PIL import Image
import moviepy.editor as mp

from django.core.cache import cache


@app.task(name='run_loop')
def run_loop():
    gif_queue = cache.get('gif_queue')
    # print(len(gif_queue) > 0)
    if len(gif_queue) > 0:
        gif_id = gif_queue.pop(0)
        cache.set("gif_queue", gif_queue, timeout=None)
        gif = Gif.objects.get(pk=gif_id)
        gif.post_to = True
        gif.save()
    print (cache.get('gif_queue'))

@shared_task()
def gif_to_jpg(path):
    print (settings.MEDIA_ROOT)
    print (path)
    new_path = path.split('.')[0]
    im = Image.open(path)
    bg = Image.new("RGB", im.size, (255,255,255))
    bg.paste(im, (0,0))
    bg.save("%s.jpg"%new_path, quality=95)

@shared_task()
def gif_to_mp4(path):
    new_path = path.split('.')[0]
    try:
        clip = mp.VideoFileClip(path)
        clip.write_videofile("%s.mp4"%new_path)
    except OSError:
        pass

@shared_task()
def add_to_cache(gif_id):
    gif_queue = cache.get("gif_queue")
    if not gif_queue:
        cache.set("gif_queue", [gif_id], timeout=None)
    else:
        gif_queue.append(gif_id)
        cache.set("gif_queue", gif_queue, timeout=None)
    print (cache.get("gif_queue"))


# @app.task
# def add_to_db(self, gif_id):
#     gif = Gif.objects.get(pk=gif_id)
#     gif.post_to = True
#     gif.save()

# @shared_task()
# def add_to_db(gif_id):
#     # print(type(app.conf.beat_schedule))
#     # print(app.conf.beat_schedule)
    
#     app.conf.beat_schedule['every-minute']['args'].append(gif_id)

#     print ("add_to_db")
#     print ("args : %s" % app.conf.beat_schedule['every-minute'].get('args'))

# @app.task(name='add_to_db')
# def add_to_db():
#     print('Hooray')
#     # return args
#     # return HttpResponse(gif_id)

# @app.task(name='for_run')
# def for_run(args):
    
#     if len(app.conf.beat_schedule['every-minute'].get('args')) > 1:
#         gif_id = app.conf.beat_schedule['every-minute']['args'].pop()
#         gif = Gif.objects.get(pk=gif_id)
#         gif.post_to = True
#         gif.save()

#     print ("for_run")
#     print ("args : %s" % app.conf.beat_schedule['every-minute'].get('args'))