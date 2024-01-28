from django.urls import path
from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("search_results/", views.search_results, name="search_results"),
    path("new_page/", views.new_page, name="new_page"),
    path("random_page/", views.random_page, name="random_page"),
    path("edit//<str:title>", views.edit, name="edit"),
    path("save/", views.save, name="save")

]
