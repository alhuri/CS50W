from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("category", views.category, name="category"),
    path("create_list", views.create_list, name="create_list"),
    path("add_list", views.add_list, name="add_list"),
    path("item/<int:auction_id>", views.item, name="item"),
    path("category_list/<int:id>", views.category_list, name="category_list"),
    path("watch_list/<int:id>", views.watch_list, name="watch_list"),
    path("watch_listing", views.watch_listing, name="watch_listing"),
    path("remove_item_watch_list/<int:auction>", views.remove_item_watch_list, name="remove_item_watch_list"),
    path("place_bid/<int:auction_id>", views.place_bid, name="place_bid"),
    path("close/<int:auction_id>", views.close, name="close"),
  
    path("register", views.register, name="register")
]
