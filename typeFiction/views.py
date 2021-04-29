import json
import markdown2
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Story, Profile, Category, Chapter
from .forms import Story_Form

# HOME PAGE
def index(request):
    form = Story_Form()
    story_list = Story.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(story_list, 20)
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)
    context = {'form': form, 'stories': stories}
    return render(request, "typefiction/index.html",context)


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


# Create new Category
@login_required
def submit_cat(request):
    # Must be request via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request only."}, status=400)
    # Create new Category
    cat = Category(name = request.POST.get("name"))
    cat.save()
    return redirect("/")


# Create new STORY
@login_required
def submit_story(request):
    # Must be request via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request only."}, status=400)
    # Create new story
    form = Story_Form(request.POST)
    if form.is_valid():
            new_story = form.save(commit=False)
            new_story.author = request.user
            new_story.save()
            return redirect("story", story_id=new_story.id)
    return redirect("/")


# Create new Chapter
@login_required
def submit_chapter(request, story_id):
    # Must be request via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request only."}, status=400)
    # Create new chapter
    n = request.POST["chapter"]
    c = request.POST["content"]
    s = Story.objects.get(id=story_id)
    new_chapter = Chapter(content = c, chapter = n)
    new_chapter.save()
    s.chapters.add(new_chapter)
    return redirect("story", story_id)


# VIEW STORY PAGE
def story(request, story_id):
    try:
        story = Story.objects.get(id=story_id)
        chapters = story.chapters.all()
    except Story.DoesNotExist:
        return redirect("/")
    context = {'story': story, 'chapters': chapters}
    return render(request, 'typefiction/story.html', context)

# PROFILE PAGE
def profile(request, user_id):
    try:
        profile = User.objects.get(id=user_id).profile
        stories = Story.objects.filter(author_id=user_id).order_by("post_date")
        following = list(profile.following.all())
        follower = Profile.objects.filter(following=profile.user)
    except User.DoesNotExist:
        return redirect("/")
    context = {'profile': profile, 'stories': stories, 'following': following, 'follower': follower}
    return render(request, 'typefiction/profile.html', context)



# NEW STORY PAGE
def new(request):
    form = Story_Form()
    context = {'form': form}
    return render(request, "typefiction/new.html", context)

# FOLLOW
@csrf_exempt
@login_required
def follow(request, user_id):
    # check if requester is in the follower list or not
    if request.method == "PUT":
        # users cannot follow themselves
        if request.user.id != user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                JsonResponse({"error": "Cannot find user."}, status=400)
            following = request.user.profile.following.all()
            if user in following:
                request.user.profile.following.remove(user_id)
                return JsonResponse({"msg": "Follow"})
            else:
                request.user.profile.following.add(user_id)
                return JsonResponse({"msg": "Unfollow"})
        JsonResponse({"error": "Cannot follow yourself."}, status=400)
    # GET method to check follower status
    # then have frontend display accordingly
    elif request.method == "GET":
        user = User.objects.get(id=user_id)
        following = request.user.profile.following.all()
        if user in following:
            return JsonResponse({"msg": "Unfollow"})
        else:
            return JsonResponse({"msg": "Follow"})
    return redirect("/")


# LIKES
@csrf_exempt
@login_required
def likes(request, story_id):
    if request.method == "PUT":
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            JsonResponse({"error": "Cannot find story."}, status=400)
        # If user already liked the story => unlike
        if request.user in story.likes.all():
            story.likes.remove(request.user)
            count = story.likes.count()
            return JsonResponse({"likes": count})
        # like
        else:
            story.likes.add(request.user.id)
            count = story.likes.count()
            return JsonResponse({"likes": count})
    return JsonResponse({"error": "PUT request only"}, status=400)