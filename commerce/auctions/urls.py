from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("category", views.category, name="category"),
    path("create_list", views.create_list, name="create_list"),
    path("add_list", views.add_list, name="add_list"),
    path("item/<int:id>", views.item, name="item"),
    path("category_list/<int:id>", views.category_list, name="category_list"),
    path("watch_list/<int:id>", views.watch_list, name="watch_list"),
    

    path("register", views.register, name="register")
]
