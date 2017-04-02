import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from PIL import Image

from .verification import is_notVerifyed

from .forms import PoolForm, RegisterForm, UploadForm, LoginForm
from .models import Gif, Like


class Pool(View):

    def get(self, request):
        show = ('show', 'hide')
        gifs = Gif.objects.all()
        is_authenticated = request.user.is_authenticated
        if is_authenticated:  
            show = ('hide', 'show')
            return render(request, "index.html", {"authenticated":request.user, "logged":is_authenticated,"show":show, "gifs":gifs})
        else:
            # return HttpResponse(show)
            return render(request, "index.html", {"authenticated": "U", "logged":is_authenticated, "show":show, "gifs":gifs})

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

        # elif request.POST.get('submit') == 'logout':
        #     logout(request)
        #     return redirect("/")

        elif request.POST.get('submit') == 'upload':
            if request.user.is_authenticated:
                # return HttpResponse(request.user.username)
                upload_form = UploadForm(request.POST, request.FILES)
                # return HttpResponse(upload_form.is_valid())
                if upload_form.is_valid():
                    creator = request.user.id
                    name = upload_form.cleaned_data['name']
                    tags = upload_form.cleaned_data['tags']
                    gif_file = upload_form.cleaned_data['gif_file']
                    #return HttpResponse(request.FILES)
                    gif = Gif.objects.create(creator=creator, name=name, tags=tags, gif_file=gif_file)
                    gif.save()
                    
                    return redirect("/")
                return HttpResponse(upload_form)
            else:
                return render(request, "index.html", {"authenticated":"False"})

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
    # model = Gif
    # template_name = 'single.html'
    # def authenticated(self, request):
    #     return request.user
    def get(self, request, pk):
        show = ('show', 'hide')
        gif = Gif.objects.get(pk=pk)
        is_authenticated = request.user.is_authenticated
        if is_authenticated:  
            show = ('hide', 'show')
            return render(request, "single.html", {"authenticated":request.user, "logged":is_authenticated,"show":show, "gif":gif})
        else:
            # return HttpResponse(show)
            return render(request, "single.html", {"authenticated": "U", "logged":is_authenticated, "show":show, "gif":gif})


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

def loved(request, pk):
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
    if request.user.is_authenticated:
        make_like(request, pk, 'loved')
        return redirect('/%s'%pk)   
    return redirect('/')

        
def laugh(request, pk):
    if request.user.is_authenticated:
        make_like(request, pk, 'laugh')
        return redirect('/%s'%pk) 
    return redirect('/')