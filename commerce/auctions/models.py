from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2,max_digits=13, blank=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    #auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.bid}$ by {self.bidder}'

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category

class Auction(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.URLField(null=True, blank=True, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTelVna9__Qwt9GifGdE0R4FmsiTmZjoSE1vnC4LXdgozvqbjiOGufuXrladHL7nXowTt4&usqp=CAU")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE,related_name="biddings", blank=True,null=True)
    start_price = models.DecimalField(decimal_places=2,max_digits=13, default=1)
    status = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.title}: {self.description} belongs to {self.category} starting with {self.start_price}"

class Comment(models.Model):
    content = models.TextField()
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.commentor} commented on {self.auction}"

class watchList(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watcher} added {self.auction}"

