from django.contrib import admin
from .models import Category, User, Auction, Bid, Comment, watchList

# Register your models here.
admin.site.register(Bid)
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(watchList)


