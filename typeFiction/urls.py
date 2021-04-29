from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("submit_cat", views.submit_cat, name="submit_cat"),
    path("submit_story", views.submit_story, name="submit_story"),
    path("submit_chapter/<int:story_id>", views.submit_chapter, name="submit_chapter"),
    path("story/<int:story_id>", views.story, name="story"),
    # LIKES
    path("likes/<int:story_id>", views.likes, name="likes"),
]
