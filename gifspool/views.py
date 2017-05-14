import random
import re
import json
from datetime import datetime, timedelta, timezone

try:
    import redis
except:
    pass
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.db.models.query import QuerySet
from PIL import Image

from .verification import is_notVerifyed

from .forms import PoolForm, RegisterForm, UploadForm, LoginForm
from .models import Gif, Like, Hashtag, GifHashtagLinker, GifView, Category
from .gifs_queue import GifsQueue

# from gifsta.celery import add_to_db
try:
    from gifspool.tasks import task_gif_to_jpg, task_gif_to_mp4, task_add_to_cache #, add_to_db
except:
    pass

from django.core.cache import cache
from django.db.models import F, Q

# gifs_queue = GifsQueue()

class MyView(View):

    def __init__(self):
        View.__init__(self)
        categories = Category.objects.filter(post_to=True)
        self.context = {"categories": categories}

    def is_authenticated(self, request=None):

        is_authenticated = request.user.is_authenticated

        if is_authenticated:  
            self.context["show"] = ('hide', 'show')
            self.context["user"] = request.user
            self.context["logged"] = is_authenticated
        else:
            self.context["show"] = ('show', 'hide')
            self.context["user"] = "U"
            self.context["logged"] = is_authenticated


class Pool(MyView):

    def __init__(self):
        MyView.__init__(self)
        self.context["use_cache"] = False
        self.context["tags"] = None

    def make_pagination(self, request, gifs_list=None, num_pages=None):
        paginator = Paginator(gifs_list, num_pages) 
        page = request.GET.get('page')
        try:
            pags = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pags = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pags = paginator.page(paginator.num_pages)
        self.context["pags"] = pags

    def update_cache(self):
        try:
            if not cache.get('gifs') or cache.get('to_update') == True:
                print("update cache")
                gifs = [model_to_dict(gif) for gif in Gif.objects.filter(post_to=True).order_by('-upload_date')]
                cache.set('gifs', gifs)
                cache.set('to_update', False)
                self.context["use_cache"] = True
            else:
                print("use cache")

            self.context["gifs"] = cache.get('gifs')

        except:
            print("get from db")
            self.context["gifs"] = Gif.objects.filter(post_to=True).order_by('-upload_date')
            self.context["use_cache"] = False
            # self.context["hashtags"] = GifHashtagLinker.objects.all()
    def get(self, request):

        Pool.update_cache(self)
        Pool.is_authenticated(self, request)
        Pool.make_pagination(self, request, self.context["gifs"], 20)
        
        return render(request, "index.html", self.context)

    def post(self, request):

        if request.POST.get('submit') == 'search':
            tags =  request.POST.get('tags').replace(" ", "+").replace("#", "%23")
            return redirect("/search?tags=%s"% tags)

        if request.POST.get('submit') == 'info':
            return redirect("/gifs")


class Gifs(View):

    def get(self, request):

        return HttpResponse(request.GET.get("info"))   

    def post(self, request):

        return HttpResponse({"gif_id":request.POST.get("gif_id"), "gif_hashtags":request.POST.get("gif_id")})          


class Upload(MyView):

    def make_tags(self, gif_obj, tags):
        for tag in re.findall(r'\#\w+', tags):
            tag = tag[1:]
            hashtag_set = Hashtag.objects.filter(hashtag = tag)
            if hashtag_set.exists():
                hashtag_set.update(count = F('count')+1)
                hashtag_obj = hashtag_set.get(hashtag = tag)
            else:
                hashtag_obj = Hashtag.objects.create(hashtag = tag)

            GifHashtagLinker.objects.create(hashtag = hashtag_obj, gif=gif_obj)



    def get(self, request):

        Upload.is_authenticated(self, request)

        if self.context["logged"]:
            return render(request, "upload.html", self.context)

        return redirect("/login")

    def post(self, request):

        if request.POST.get('submit') == 'upload':
            upload_form = UploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                creator = request.user
                name = upload_form.cleaned_data['name']
                tags = upload_form.cleaned_data['tags']
                gif_file = upload_form.cleaned_data['gif_file']
                gif = Gif.objects.create(creator=creator, name=name, tags=tags, gif_file=gif_file, post_to=False)
                Upload.make_tags(self, gif, tags)
                try:
                    task_add_to_cache.delay(gif_id = gif.id)
                    task_gif_to_jpg.delay(path = gif.gif_file.path)
                    task_gif_to_mp4.delay(path = gif.gif_file.path)
                except:
                    pass
                gif.save()

                return redirect("/")

            return HttpResponse("upload form isn't valid")
            


class Logout(MyView):

    def get(self, request):

        print(request.get_full_path())
        logout(request)
        return redirect('/')


class Login(MyView):

    def get(self, request):

        Login.is_authenticated(self, request)
        return render(request, "login.html", self.context)


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
                    return render(request, "login.html", self.context)
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    login(request, user, 'django.contrib.auth.backends.ModelBackend')
                    return redirect("/")
            return render(request, "login.html", self.context)

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
            return render(request, "login.html", self.context)


class CategoriesGifs(Pool):

    def get(self, request, category):
        # category = Category.objects.filter(name=category)[0]
        if category == 'virus':
            self.context["gifs"] = Gif.objects.all().order_by("-likes")
        else:
            kwargs = { "%s__gt"%category: 0 }
            self.context["gifs"] = Gif.objects.filter(**kwargs).order_by("-%s"%category)
        Pool.is_authenticated(self, request)
        Pool.make_pagination(self, request, self.context["gifs"], 20)
        
        return render(request, "index.html", self.context)
    


class Tags(Pool):

    def find_brute(tags=None):
        print(type(tags))
        if isinstance(tags, list):
            q_object = Q()
            for tag in tags:
                tag = tag[1:]
                q_object |= Q(hashtag = tag)
            hashtag_set = Hashtag.objects.filter(q_object)
        elif isinstance(tags, QuerySet):
            if tags.count() < 1:
                return tags
            hashtag_set = tags

        q_object = Q()
        for hashtag in hashtag_set:
            q_object |= Q(hashtag = hashtag.id)
        linkers = GifHashtagLinker.objects.filter(q_object)

        q_object = Q()
        for linker in linkers:
            q_object |= Q(gifhashtaglinker = linker.id)
        gifs = Gif.objects.filter(q_object).order_by('-upload_date')
        
        return gifs

    def get(self, request):
    # def get(self, request, tags):

        self.context['gifs'] = None
        tags = re.findall(r'\#\w+', request.GET.get('tags'))
        # tags = re.findall(r'\#\w+', tags)
        if len(tags) > 0:
            gifs = Tags.find_brute(tags)
            # return HttpResponse(gifs.id)
            # return HttpResponse(gifs)
            
            self.context['gifs'] = gifs
            Tags.is_authenticated(self, request)
            Pool.make_pagination(self, request, self.context["gifs"], 20)
        # return HttpResponse(self.context['gifs'][0].id)
        return render(request, "index.html", self.context)

class OneGif(Tags):
    
    def make_view(self, gif, user, ip_address):
        gif.views += 1
        gif.save()
        try:
            view = GifView.objects.get(gif=gif)
        except GifView.DoesNotExist:
            view = None
        if view:
            view.view_date = datetime.now(timezone.utc)
            view.save()
        else:
            GifView.objects.create(gif=gif, user=user, ip_address=ip_address)
        

    def make_related(self, gif):
        related = list(OneGif.find_brute(gif.hashtags.all()))
        if len(related) > 4:
            self.context['related'] = []
            while len(self.context['related']) < 4:
                rand = random.choice(related)
                if rand not in self.context['related']:
                    self.context['related'].append(rand)
        else:
            self.context['related'] = related

    def make_next_prev(self, gif):
        try:
            self.context['prev_gif'] = Gif.objects.get(pk=gif.prev_gif)
        except (NameError, Gif.DoesNotExist):
            pass

        try:
            self.context['next_gif'] = Gif.objects.get(pk=gif.next_gif)
        except (NameError, Gif.DoesNotExist):
            pass

    def get(self, request, pk, name):

        gif = get_object_or_404(Gif,pk=pk)
        # gif = Gif.objects.get(pk=pk)
        user = request.user
        ip_address = request.META['REMOTE_ADDR']

        OneGif.make_view(self, gif, user, ip_address)
        OneGif.make_related(self, gif)
        OneGif.make_next_prev(self, gif)

        self.context['gif'] = gif
        
        

        OneGif.is_authenticated(self, request)

        return render(request, "single.html", self.context)

    def post(self, request, pk):

        if request.POST.get('submit') == 'search':

            tags =  request.POST.get('tags').replace(" ", "+").replace("#", "%23")

            return redirect("/search?tags=%s"% tags)


class Best(Pool):

    def by_day(self):
        q_object = Q()
        q_object &= Q(upload_date__gt= (datetime.now(timezone.utc)- timedelta(days=1)))
        q_object &= Q(post_to=True)
        return q_object

    def by_week(self):
        q_object = Q()
        q_object &= Q(upload_date__gt= (datetime.now(timezone.utc)- timedelta(days=7)))
        q_object &= Q(post_to=True)
        return q_object

    def by_mounth(self):
        q_object = Q()
        q_object &= Q(upload_date__gt= (datetime.now(timezone.utc)- timedelta(days=30)))
        q_object &= Q(post_to=True)
        return q_object

    def get(self, request, period):
        q_object = Q(post_to=True)

        if period == 'day':
            q_object = Best.by_day(self)
        elif period == 'week':
            q_object = Best.by_week(self)
        elif period == 'month':
            q_object = Best.by_mounth(self)

        self.context["gifs"] = Gif.objects.filter(q_object).order_by('-upload_date')
        self.context["use_cache"] = False
        Pool.make_pagination(self, request, self.context["gifs"], 20)
        Pool.is_authenticated(self, request)
        # return HttpResponse(self.context["gifs"][0].upload_date >= (datetime.now(timezone.utc)- timedelta(days=1)))#-timedelta(days=1))#
        return render(request, 'index.html', self.context)


def make_like(user, pk, index):
    kwargs = {}
    kwargs[index] = True
    
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
        # try:
        #     like = likes[0]
        #     if getattr(like, index) == True:
        #         val = lambda x: x-1 if x > 0 else 0
        #         setattr(like, index, False)
        #         setattr(gif, index, val(getattr(gif, index)))
        #     elif getattr(like, index) == False:
        #         setattr(like, index, True)
        #         setattr(gif, index, getattr(gif, index)+1)
        # except NameError:
        #     pass
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

    return {"shocked":gif.shocked, "loved":gif.loved, "laugh":gif.laugh, "likes":gif.likes, "views":gif.views }

def shocked(request, pk, name):
    print(pk)
    if request.user.is_authenticated:
        user = request.user
        make_like(user, pk, 'shocked')
        return redirect('/%s-%s'%(pk, name))
    return redirect('/login')

def laugh(request, pk, name):
    print(pk)
    if request.user.is_authenticated:
        user = request.user
        make_like(user, pk, 'laugh')
        return redirect('/%s-%s'%(pk, name))
    return redirect('/login')

def loved(request, pk, name):
    print(pk)
    if request.user.is_authenticated:
        user = request.user
        make_like(user, pk, 'loved')
        return redirect('/%s-%s'%(pk, name))   
    return redirect('/login')
    
def likes_ajax(request):
    
    if request.is_ajax() and request.POST:
        response = {'authenficated': 'False'}
        if request.user.is_authenticated:
            print(request.POST['pk'], request.POST['name'], request.POST['index'])
            pk = request.POST['pk']
            name = request.POST['name']
            index = request.POST['index']
            user = request.user
            response = make_like(user, pk, index)
            print(response)
            response['authenficated'] = 'True'
            
        return JsonResponse(response)
    else:
        raise Http404
   
def see_cache(request):
    # return HttpResponse(cache.get('gifs'))
    return HttpResponse([model_to_dict(gif) for gif in Gif.objects.filter(post_to=True).order_by('-upload_date')[0:1]])


def ajax(request):
    return render(request, "ajax.html", {})

def add_ajax(request):
    print('hui')
    return JsonResponse({'first-text': 'wtf', 'second-text': 'fuckoff'})
    # if request.method=='get':
    #     response = {'first-text': 'wtf', 'second-text': 'fuckoff'}
    #     return JsonResponse(response)
    # else:
    #     return Http404

def cookies_page(request):
    return HttpResponse(request.COOKIES)

def set_cookies(request):
    response = redirect("/cookies")
    response.set_cookie("hui","vam")
    return response

def session_page(request):
    return HttpResponse(request.session['has_commented'])

def set_session(request):

    request.session['has_commented'] = True
    return redirect("/session")
