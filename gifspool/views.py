import re
import json
import redis
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from PIL import Image

from .verification import is_notVerifyed

from .forms import PoolForm, RegisterForm, UploadForm, LoginForm
from .models import Gif, Like
from .gifs_queue import GifsQueue

# from gifsta.celery import add_to_db
from gifspool.tasks import gif_to_jpg, gif_to_mp4, add_to_cache #, add_to_db

from django.core.cache import cache


# gifs_queue = GifsQueue()

class Pool(View):

    context = {"user": "U", 
               "logged": None, 
               "show": ('show', 'hide'), 
               "use_cache": False,
               "tags": None,
               }

    def get(self, request):

        is_authenticated = request.user.is_authenticated
        # cache.get('gifs')
        try:
            if not cache.get('gifs') or cache.get('to_update') == True:
                print("update cache")
                cache.set('gifs', [gif.__dict__ for gif in Gif.objects.filter(post_to=True)])
                Pool.context["gifs"] = cache.get('gifs')
                cache.set('to_update', False)
                Pool.context["use_cache"] = True
                # context["gifs"] = Gif.objects.filter(post_to=True)
            else:
                print("use cache")
                Pool.context["gifs"] = cache.get('gifs')
        except redis.exceptions.ConnectionError:
            print("get from db")
            Pool.context["gifs"] = Gif.objects.filter(post_to=True)
            Pool.context["use_cache"] = False
            # return HttpResponse([gif.__dict__ for gif in gifs][0]['id'])
        # else:
        #     return HttpResponse(cache.get('gifs')[0]['name'])
        # return HttpResponse(Gif._meta.get_fields())
        # return HttpResponse(settings.MEDIA_ROOT)
        
        if is_authenticated:  
            Pool.context["show"] = ('hide', 'show')
            Pool.context["user"] = request.user
            Pool.context["logged"] = is_authenticated
            return render(request, "index.html", Pool.context)
        else:
            return render(request, "index.html", Pool.context)

    def post(self, request):

        if request.POST.get('submit') == 'register':
            register_form = RegisterForm(request.POST)
            #return HttpResponse(register_form.errors.values())
            if register_form.is_valid():
                #return HttpResponse(register_form.cleaned_data)
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password']
                confirm = register_form.cleaned_data['confirm']
                email = register_form.cleaned_data['email']
                is_not = is_notVerifyed(username, password, confirm, email, User)
                if is_not:
                    return render(request, "index.html", is_not)
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    login(request, user, 'django.contrib.auth.backends.ModelBackend')
                    return redirect("/")
            return render(request, "index.html", {})

        elif request.POST.get('submit') == 'login':
            login_form = LoginForm(request.POST)
            #return HttpResponse(login_form.errors.values())
            if login_form.is_valid():
                #return HttpResponse(login_form.cleaned_data.keys())
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
            return redirect("/")

        elif request.POST.get('submit') == 'search':

            tags =  request.POST.get('tags').replace(" ", "")

            return redirect("/tags/%s/"% tags)
            


class Upload(View):

    context = {"user": "U", 
               "logged": None, 
               "show":('show', 'hide'), 
               # "gifs_queue":gifs_queue,
               }

    def get(self, request):

        is_authenticated = request.user.is_authenticated

        try:
            if not cache.get('gifs'):
                gifs = Gif.objects.filter(post_to=True)
                cache.set('gifs', [gif.__dict__ for gif in gifs])
                Upload.context["gifs"] = cache.get('gifs')
                # context["gifs"] = Gif.objects.filter(post_to=True)
            else:
                Upload.context["gifs"] = cache.get('gifs')
        except:
            Upload.context["gifs"] = Gif.objects.filter(post_to=True)

        if is_authenticated:  
            Upload.context["show"] = ('hide', 'show')
            Upload.context["user"] = request.user
            return render(request, "upload.html", Upload.context)
        else:
            # 
            return render(request, "upload.html", Upload.context)

    def post(self, request):

        if request.POST.get('submit') == 'upload':
            is_authenticated = request.user.is_authenticated
            if is_authenticated:
                # return HttpResponse(request.user.username)
                upload_form = UploadForm(request.POST, request.FILES)
                # return HttpResponse(request.FILES)
                if upload_form.is_valid():
                    creator = request.user
                    name = upload_form.cleaned_data['name']
                    tags = upload_form.cleaned_data['tags']
                    gif_file = upload_form.cleaned_data['gif_file']
                    #return HttpResponse(request.FILES)
                    gif = Gif.objects.create(creator=creator, name=name, tags=tags, gif_file=gif_file, post_to=False)
                    add_to_cache.delay(gif_id = gif.id)
                    gif_to_jpg.delay(path = gif.gif_file.path)
                    gif_to_mp4.delay(path = gif.gif_file.path)
                    gif.save()
                    
                    return redirect("/")

                return render(request, "upload.html", Upload.context)
            else:
                return render(request, "index.html", Upload.context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class Login(View):
    def get(slef, request):
        return render(request, "login.html", {})
    def post(slef, request):
        if request.POST.get('submit') == 'login':
            login_form = LoginForm(request.POST)
            #return HttpResponse(login_form.errors.values())
            if login_form.is_valid():
                #return HttpResponse(login_form.cleaned_data.keys())
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
            else:
                return render(request, "index.html", {})


class OneGif(View):
    context = {"user": "U", 
               "logged": None, 
               "show": ('show', 'hide'), 
               # "gifs_queue":gifs_queue,
               }
    def get(self, request, pk):

        OneGif.context['gif'] = Gif.objects.get(pk=pk)
        is_authenticated = request.user.is_authenticated
        if is_authenticated:  
            OneGif.context["show"] = ('hide', 'show')
            OneGif.context["user"] = request.user
            OneGif.context["logged"] = is_authenticated
            return render(request, "single.html", OneGif.context)
        else:
            return render(request, "single.html", OneGif.context)

class Tags(View):
    context = {"user": "U", 
               "logged": None, 
               "show": ('show', 'hide'), 
               # "gifs_queue":gifs_queue,
               }
    def get(self, request, tags):

        gifs = Gif.objects.all()

        for tag in tags.split("#"):
            gifs = gifs.filter(tags=tag)

        Tags.context['gifs'] = gifs
        is_authenticated = request.user.is_authenticated

        if is_authenticated:  
            Tags.context["show"] = ('hide', 'show')
            Tags.context["user"] = request.user
            Tags.context["logged"] = is_authenticated
            return render(request, "index.html", Tags.context)


def make_like(request, pk, index):
    kwargs = {}
    kwargs[index] = True
    user = request.user
    gif = get_object_or_404(Gif, pk=pk)
    #return HttpResponse(len(Like.objects.filter(gif_id=pk, user_id=user.id)))
    likes = Like.objects.filter(gif_id=gif, user_id=user)
    if not likes:
        like = Like.objects.create(gif_id=gif, user_id=user, **kwargs)
        like.save()
        setattr(gif, index, getattr(gif, index)+1)
        # gif.loved += 1
        # gif.likes = gif.shocked + gif.loved + gif.laugh
        # gif.save()
        # return redirect('/%s'%pk)
    else:
        for field in likes[0]._meta.get_fields():
            # return HttpResponse(getattr(likes[0], field.name))
            if getattr(likes[0], field.name) == True:
                # return HttpResponse(field.name)
                likes.delete()
                val = lambda x: x-1 if x > 0 else 0
                if field.name == index:
                    setattr(gif, index, val(getattr(gif, index)))
                    # # gif.likes = gif.shocked + gif.loved + gif.laugh
                    # gif.save()
                    # return redirect('/%s'%pk)
                else:
                    like = Like.objects.create(gif_id=gif, user_id=user, **kwargs)#**kwargs)
                    like.save()
                    setattr(gif, field.name, val(getattr(gif, field.name)))
                    setattr(gif, index, getattr(gif, index)+1)
                    # gif.likes = gif.shocked + gif.loved + gif.laugh
                    # gif.save()
                    # return redirect('/%s'%pk)
                break
    gif.likes = gif.shocked + gif.loved + gif.laugh
    gif.save()

def shocked(request, pk):
    if request.user.is_authenticated:
        make_like(request, pk, 'shocked')
        return redirect('/%s'%pk)
    return redirect('/')

def laugh(request, pk):
    if request.user.is_authenticated:
        make_like(request, pk, 'laugh')
        return redirect('/%s'%pk) 
    return redirect('/')

def loved(request, pk):
    if request.user.is_authenticated:
        make_like(request, pk, 'loved')
        return redirect('/%s'%pk)   
    return redirect('/')
    # #return HttpResponse(pk)
    # if request.user.is_authenticated:
    #     user = request.user
    #     gif = get_object_or_404(Gif, pk=pk)
    #     #return HttpResponse(len(Like.objects.filter(gif_id=pk, user_id=user.id)))
    #     likes = Like.objects.filter(gif_id=gif, user_id=user)
    #     if not likes:
    #         like = Like.objects.create(gif_id=gif, user_id=user, loved=True)
    #         like.save()
    #         gif.loved += 1
    #         # gif.likes = gif.shocked + gif.loved + gif.laugh
    #         # gif.save()
    #         # return redirect('/%s'%pk)
    #     else:
    #         for field in likes[0]._meta.get_fields():
    #             # return HttpResponse(getattr(likes[0], field.name))
    #             if getattr(likes[0], field.name) == True:
    #                 # return HttpResponse(field.name)
    #                 if field.name == "loved":
    #                     likes.delete()
    #                     if gif.loved > 0:
    #                         gif.loved -= 1
    #                         # # gif.likes = gif.shocked + gif.loved + gif.laugh
    #                         # gif.save()
    #                         # return redirect('/%s'%pk)
    #                 else:
    #                     likes.delete()
    #                     kwargs = {}
    #                     kwargs[field.name] = True
    #                     like = Like.objects.create(gif_id=gif, user_id=user, loved=True)#**kwargs)
    #                     like.save()
    #                     val = lambda x: x-1 if x > 0 else 0
    #                     setattr(gif, field.name, val(getattr(gif, field.name)))
    #                     gif.loved += 1
    #                     # gif.likes = gif.shocked + gif.loved + gif.laugh
    #                     # gif.save()
    #                     # return redirect('/%s'%pk)
    #                 break
    #     gif.likes = gif.shocked + gif.loved + gif.laugh
    #     gif.save()
    

        
