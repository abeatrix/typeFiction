from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    # PROFILE
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/edit/<int:user_id>", views.profile_edit, name="profile_edit"),
    path("submit_cat", views.submit_cat, name="submit_cat"),
    path("submit_story", views.submit_story, name="submit_story"),
    path("story/<int:story_id>", views.story, name="story"),
    path("submit_chapter/<int:story_id>", views.submit_chapter, name="submit_chapter"),
    path("submit_comment/<int:story_id>", views.submit_comment, name="submit_comment"),
    # LIKES
    path("likes/<int:story_id>", views.likes, name="likes"),
    # FOLLOWS
    path("follows/<int:user_id>", views.follows, name="follows"),
    # WATCHLIST
    path("watchlist/<int:story_id>", views.watchlist, name="watchlist"),
]
