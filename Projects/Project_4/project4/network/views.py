import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator

from .models import User, Post, Profile


def index(request):
    posts = Post.objects.all().order_by('-time')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            profile = Profile(
                user=user
            )
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def following(request):
    profile = Profile.objects.filter(user=User.objects.get(username=request.user.username))
    followings = profile[0].followings.all()
    posts = Post.objects.filter(poster__in=followings).order_by('-time')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "profile": profile[0],
        "posts": page_obj
    })

def profile_view(request, username):
    user = User.objects.filter(username=username)
    if not user:
        return HttpResponseRedirect(reverse("index"))

    posts = Post.objects.filter(poster=user[0]).order_by('-time')
    profile = Profile.objects.filter(user=user[0])

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "user": user[0],
        "posts": page_obj,
        "profile": profile[0],
        "is_following": str(request.user in profile[0].followers.all()).lower()
    })


@csrf_exempt
@login_required
def post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    poster = User.objects.get(username = data.get("poster", ""))
    content = data.get("content", "")
    time = datetime.now()

    try:
        post = Post(
            poster = poster,
            content = content,
            time = time
        )
        post.save()
        return JsonResponse({"message": "Content Posted Successfully"}, status=200)

    except:
        return JsonResponse({"message": "An Error Occured"}, status=400)


@csrf_exempt
@login_required
def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    mainuser = User.objects.get(username = data.get("mainuser", ""))
    targetuser = User.objects.get(username = data.get("targetuser", ""))
    status = data.get("status", "")

    # print(data)
    is_following = targetuser in Profile.objects.filter(user=mainuser)[0].followings.all()
    # print(is_following)

    try:
        if status == "Follow" and not is_following:
            print("follow process")
            Profile.objects.get(user=mainuser).followings.add(targetuser) 
            Profile.objects.get(user=targetuser).followers.add(mainuser) 
            return JsonResponse({"message": "Follow Successful"}, status=200)

        elif status == "Unfollow" and is_following:
            print("Unfollow process")
            Profile.objects.get(user=mainuser).followings.remove(targetuser) 
            Profile.objects.get(user=targetuser).followers.remove(mainuser) 
            return JsonResponse({"message": "Unfollow Successful"}, status=200)
    except:
        return JsonResponse({"message": "An Error Occured"}, status=400)


@csrf_exempt
@login_required
def edit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        data = json.loads(request.body)
        post = Post.objects.get(id=data.get("post_id",""))
        newContent = data.get("content", "")

        post.content = newContent
        post.save()
        return JsonResponse({"message": "Edit Successful"}, status=200)
    except:
        return JsonResponse({"message": "An Error Occured"}, status=400)


@csrf_exempt
@login_required
def like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        data = json.loads(request.body)
        user = User.objects.get(username = data.get("user", ""))
        post = Post.objects.get(id= data.get("post_id", ""))
        condition = data.get("condition","")

        if condition == "Like":
            post.likers.add(user)
            return JsonResponse({"message": "Like Successful"}, status=200)
        elif condition == "Unlike":
            post.likers.remove(user)
            return JsonResponse({"message": "Unlike Successful"}, status=200)

    except:
        return JsonResponse({"message": "An Error Occured"}, status=400)
