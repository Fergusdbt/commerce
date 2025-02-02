from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("watchlist/<str:username>", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category")
]
