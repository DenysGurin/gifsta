from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .verification import is_notVerifyed
from .forms import PoolForm, RegisterForm, UploadForm
from .models import Gif

class Pool(View):

    def get(self, request):
        show = ('show', 'hide')
        gifs = Gif.objects.all()
        if request.user.is_authenticated:
            
            show = ('hide', 'show')
            return render(request, "pool.html", {"authenticated":request.user, "show":show, "gifs":gifs})
        else:
            # return HttpResponse(show)
            return render(request, "pool.html", {"authenticated":"False", "show":show, "gifs":gifs})
    def post(self, request):
        if request.POST.get('submit') == 'register':
            register_form = RegisterForm(request.POST)

            if register_form.is_valid():
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password']
                confirm = register_form.cleaned_data['confirm']
                email = register_form.cleaned_data['email']
                is_not = is_notVerifyed(username, password, confirm, email, User)
                if is_not:
                    return render(request, "pool.html", is_not)
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    login(request, user, 'django.contrib.auth.backends.ModelBackend')
                    return redirect("/")
            return render(request, "pool.html", is_not)

        elif request.POST.get('submit') == 'login':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            elif user is None:
                return render(request, "pool.html", {})

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
                    gif = Gif.objects.create(creator=creator, name=name, tags=tags, gif_file=gif_file)
                    gif.save()
                    
                    return redirect("/")
                return HttpResponse(upload_form)
            else:
                return render(request, "pool.html", {"authenticated":"False"})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")