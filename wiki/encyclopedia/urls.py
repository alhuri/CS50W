from django.urls import path
from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("search_results/", views.search_results, name="search_results"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("save_changes/", views.save_changes, name="save_changes"),
    path("random_page/", views.random_page, name="random_page")
]
