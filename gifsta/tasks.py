from django.http import HttpResponse
from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
# from .views import gifs_queue
from gifspool.models import Gif
from celery import Celery, shared_task

# from .celery import app


# # @periodic_task(run_every=(crontab(minute='*/1')), name="add_to_db", ignore_result=True)
# @app.task
# def add_to_db(gif_id):
#     # # do something
#     # gif = Gif.objects.get(pk=gif_id)
#     # gif.post_to = True
#     # gif.save()
#     print (gif_id)
#     # return HttpResponse(gif_id)
