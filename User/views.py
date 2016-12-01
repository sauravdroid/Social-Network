from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .form_auth import CustomUserForm, LoginForm, PostForm
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from Friends.models import Friend, RequestList
from Friends.status import Status
from django.utils import timezone
from django.db import IntegrityError
from Post.models import Post, PostLikes


def register_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.is_admin = True
            user.save()
            return HttpResponse("Registration Successful")
    else:
        form = CustomUserForm()
    return render(request, "User/register.html", {"form": form, "button_text": "Register"})


def login_user(request):
    if request.user.is_authenticated():
        return redirect('user:profile', user_email=request.user.email)
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(email=email, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        if request.GET.get(
                                'next'):  # To check if the user tried to access a page where login was required
                            return redirect(request.GET.get('next'))
                        return redirect('user:profile', user_email=email)
                    else:
                        return HttpResponse("User is In active")
                else:
                    return HttpResponse("User is not registered")
        else:
            form = LoginForm()
    return render(request, "User/register.html", {"form": form, "button_text": "Login"})


def logout_user(request):
    logout(request)
    return redirect('user:login')


@login_required(login_url='user:login', redirect_field_name='')
def user_profile(request, user_email):
    if request.method == 'GET':
        form = PostForm()
        userFK = get_object_or_404(CustomUser, email=user_email)
        if not request.user.friend_set.filter(friend_email=user_email):
            is_friend="false"
        else:
            is_friend="true"
        posts = userFK.post_set.all().order_by('-created_at')
        users = CustomUser.objects.all()

        if request_already_sent(request, user_email) and can_send_request(request, user_email):
            request_permission = "true"
        else:
            request_permission = "false"
        if request.GET.get('query'):
            starts_with = request.GET.get('query')
            try:
                users = CustomUser.objects.filter(email__startswith=starts_with)
            except ObjectDoesNotExist:
                return HttpResponse('<h5>No user matching your query</h5>')
            return render(request, "User/all_user.html", {"users": users, "current_user": request.user.email,
                                                          "username": request.user.email.split('@')[0]})
        if request.user.email == user_email:
            # If user is the logged in user
            return render(request, "User/profile_new.html",
                          {"full_name": request.user.get_full_name(), "form": form, "posts": posts,
                           "create_post": "true", "email": request.user.get_short_name(), "users": users,
                           "username": request.user.email.split('@')[0],
                           "friend_requests": get_pending_request(request),})
        else:
            # If user is not the logged in user
            return render(request, "User/profile_new.html",
                          {"full_name": request.user.get_full_name(), "posts": posts, "create_post": "false",
                           "email": request.user.email, "users": users,
                           "username": request.user.email.split('@')[0], "user_email": user_email,
                           "can_send_request": request_permission,"is_friend":is_friend})

    if request.method == 'POST':
        if request.POST.get('create', False):
            form = PostForm(request.POST)
            if form.is_valid():
                users = form.save(commit=False)
                users.user = request.user
                users.save()
                return redirect('user:profile', user_email=user_email)
            return HttpResponse("Error Occured")


        elif request.POST.get('logout'):
            logout(request)
            return redirect('user:login')


        elif request.POST.get("add_friend"):
            if send_request(request, user_email):
                return HttpResponse("Request successfully sent")
            return HttpResponse("Request already sent")


        elif request.POST.get("accept_request"):
            requested_user_email = request.POST.get("accept_request")
            accept_request(request, requested_user_email)
            return redirect('user:profile', user_email=request.user.email)


        elif request.POST.get("edit_post"):
            return HttpResponse("Edit Post")


        elif request.POST.get("like_post"):
            try:
                post_id = request.POST.get("like_post")
                post = Post.objects.get(id=post_id)
                post_likes = PostLikes(user=request.user, post=post, liked_at=timezone.now(),
                                       user_email=request.user.email,
                                       post_id_meta=post_id)
                post_likes.save()
                post.likes += 1
                post.save()
            except IntegrityError as e:
                return redirect('user:profile', user_email=user_email)
            return redirect('user:profile', user_email=user_email)


def show_profile(request):
    return render(request, "User/profile_user.html", {"form": None})


@login_required(login_url='user:login')
def get_all_users(request):
    users = CustomUser.objects.all()
    return render(request, "User/all_user.html",
                  {"users": users, "current_user": request.user.email, "username": request.user.email.split('@')[0]})


@login_required(login_url='user:login')
def create_article(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('user:profile', user_email=request.user.email)
    return render(request, 'User/create_article.html',
                  {"form": form, "email": request.user.email, "username": request.user.email.split('@')[0]})


def send_request(request, user_email):
    # request:Current user ,user_email:Email of the visited user.
    try:
        requested_user = CustomUser.objects.get(email=user_email)
        request_list = RequestList(user=requested_user, user_email=user_email, requested_user_email=request.user.email,
                                   request_date=timezone.now(), request_type=Status.pending())
        request_list.save()
    except IntegrityError as e:
        return False
    return True


def can_send_request(request, user_email):
    requested_user = RequestList.objects.filter(requested_user_email=user_email, user_email=request.user.email)
    if len(requested_user) == 0:
        return True
    else:
        return False


def request_already_sent(request, user_email):
    requested_user = RequestList.objects.filter(user_email=user_email, requested_user_email=request.user.email)
    if len(requested_user) == 0:
        return True
    else:
        return False


def get_pending_request(request):
    friend_request = RequestList.objects.filter(user_email=request.user.email, request_type=Status.pending())
    return friend_request


def accept_request(request, user_email):
    requested_user = CustomUser.objects.get(email=user_email)
    friend1 = Friend(user=request.user, user_email=request.user.email, friend_email=user_email, friend_type="normal",
                     request_type=Status.accepted(), friend_since=timezone.now())
    friend2 = Friend(user=requested_user, user_email=user_email, friend_email=request.user.email, friend_type="normal",
                     request_type=Status.accepted(), friend_since=timezone.now())
    requestList = RequestList.objects.get(user_email=request.user.email, requested_user_email=user_email)
    requestList.request_type = Status.accepted()
    requestList.save()
    friend1.save()
    friend2.save()


@login_required(login_url='user:login')
def show_friends(request):
    friends = Friend.objects.filter(user_email=request.user.email)
    return render(request, "User/friends.html",
                  {"username": request.user.email.split('@')[0], "email": request.user.email, "friends": friends})
