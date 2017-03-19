from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .verification import is_notVerifyed
from .forms import PoolForm, RegisterForm

class Pool(View):

    def get(self, request):
        show = ('show', 'hide')
        if request.user.is_authenticated:
            show = ('hide', 'show')
            return render(request, "pool.html", {"authenticated":request.user, "show":show})
        else:
            return render(request, "pool.html", {"authenticated":"False", "show":show})
    def post(self, request):
        if request.POST.get('submit') == 'registration':
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

        elif request.POST.get('submit') == 'logout':
            logout(request)
            return redirect("/")