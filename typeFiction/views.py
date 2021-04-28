import json
import markdown2
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Story, Profile, Category


def index(request):
    return render(request, "typefiction/index.html")


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
            return render(request, "typefiction/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "typefiction/login.html")


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
            return render(request, "typefiction/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "typefiction/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "typefiction/register.html")


# STORY
@login_required
def create(request):
    # Must be request via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request only."}, status=400)
    # Create new story
    title = request.POST.get("title")
    description = request.POST.get("description")
    category = request.POST.get("category")
    story = Post(author=request.user, title=title, description=description, category=category)
    post.save()
    # redirect to profile page after post is created
    return redirect('profile', user_id=request.user.id)
    # return JsonResponse({"message": "Post created successfully"}, status=201)