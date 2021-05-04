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

from .models import User, Story, Profile, Category, Chapter, Comment
from .forms import Story_Form, Comment_Form, Chapter_Form, Profile_Form

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



# ------- AUTH -------#

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



# ------- CATEGORY -------#

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



# ------- STORY -------#

# VIEW STORY PAGE
def story(request, story_id):
    try:
        story = Story.objects.get(id=story_id)
        chapters = story.chapters.all()
        comments = Comment.objects.filter(story_id=story_id, reply=None)
    except Comment.DoesNotExist:
        comments = None
    except Story.DoesNotExist:
        return redirect("/")
    context = {'story': story, 'chapters': chapters, 'comments': comments}
    return render(request, 'typefiction/story.html', context)


# NEW STORY PAGE
def new(request):
    form = Story_Form()
    context = {'form': form}
    return render(request, "typefiction/new.html", context)


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
    new_chapter = Chapter(content = c, chapter = n, story = s)
    new_chapter.save()
    s.chapters.add(new_chapter)
    return redirect("story", story_id)


# EDIT STORY
@login_required
def story_edit(request, story_id):
    # Must be request via PUT
    story = Story.objects.get(id=story_id)
    # TO UPDATE THE NEWLY EDITED STORY
    if request.method == "POST" and request.user == story.author:
        story_form = Story_Form(request.POST, instance=story)
        if story_form.is_valid():
            story_form.save()
            return redirect('story', story_id)
    # GET story details for editing purpose
    elif request.method == "GET" and request.user == story.author:
        story_form = Story_Form(instance=story)
        context = {'form': story_form, 'story': story}
        return render(request, "typefiction/new.html", context)


# DELETE STORY
@login_required
def delete_story(request, story_id):
    story = Story.objects.get(id=story_id)
    if story.user == request.user:
        story.delete()
    return redirect('story', story_id=story_id)


# EDIT CHAPTER
@login_required
def story_edit(request, story_id, chapter_id):
    # Must be request via PUT
    chapter = Chapter.objects.get(id=chapter_id)
    # TO UPDATE THE NEWLY EDITED CHAPTER
    if request.method == "POST" and request.user == chapter.story.author:
        c_form = Chapter_Form(request.POST, instance=chapter)
        if c_form.is_valid():
            c_form.save()
            return redirect('story', story_id)
    # GET chapter details for editing purpose
    elif request.method == "GET" and request.user == chapter.story.author:
        c_form = Chapter_Form(instance=chapter)
        context = {'form': c_form, 'chapter': chapter}
        return render(request, "typefiction/new.html", context)

# DELETE CHAPTER
@login_required
def delete_chapter(request, story_id, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    if chapter.story.user == request.user:
        chapter.delete()
    return redirect('story', story_id=story_id)


# ------- COMMENTS / REVIEWS -------#

# Create Comments
@login_required
def submit_comment(request, story_id):
    comment_form = Comment_Form(data=request.POST)
    story = Story.objects.get(id=story_id)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.story_id = story_id
        new_comment.story = story
        new_comment.save()
        return redirect('story', story_id=story_id)


# Delete Comment
@login_required
def delete_comment(request, story_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        Comment.objects.get(id=comment_id).delete()
        return redirect('story', story_id=story_id)
    return redirect('story', story_id=story_id)



# ------- PROFILE -------#

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


# FOLLOWS
@csrf_exempt
@login_required
def follows(request, user_id):
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
            story.likes.add(request.user)
            count = story.likes.count()
            return JsonResponse({"likes": count})
    return JsonResponse({"error": "PUT request only"}, status=400)

# ADD TO WATCHLIST
@csrf_exempt
@login_required
def watchlist(request, story_id):
    # check if requester is in the follower list or not
    if request.method == "PUT":
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            JsonResponse({"error": "Cannot find story."}, status=400)
        # users cannot follow themselves
        if request.user.id != story.author.id:
            watchers= story.watchlist.all()
            if request.user in watchers:
                story.watchlist.remove(request.user)
                msg = "Add to Watchlist"
            else:
                story.watchlist.add(request.user)
                msg = "Remove from Watchlist"
            return JsonResponse({"msg": msg, "count": story.watchlist.count()})
        JsonResponse({"error": "Cannot add your own story to watchlist."}, status=400)
    return redirect("/")
