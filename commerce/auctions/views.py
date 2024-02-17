from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Auction,watchList
from django.views.generic import CreateView
from django import forms
from django.forms import formset_factory


CHOICES = Category.objects.values_list()

class AuctionForm(forms.Form):
    title = forms.CharField(max_length=32)
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    start_price = forms.DecimalField()
    image = forms.URLField(label="Image URL", initial="http://", required=False)
    category = forms.ChoiceField(choices = CHOICES)

auction_form = AuctionForm()


def index(request):
    active = Auction.objects.filter(status=True)
    return render(request, "auctions/index.html",{
        "active_listings": active
        })

def item(request,id):
    item = Auction.objects.get(pk=id)
    return render(request, "auctions/item.html",{
        "item": item
        })

def create_list(request):
    return render(request, "auctions/create_list.html",{
        'form': auction_form
    })

def watch_list(request, id):
    auction = Auction.objects.get(pk=id)

    watchlist = watchList(
                watcher = User.objects.get(pk=request.user.id),
                auction = auction
            )
    watchlist.save()

    list = watchList.objects.get(pk=request.user.id)
    
    return render(request, "auctions/watch_list.html",{
        "active_listings": list
        })

def add_list(request):
    if request.method == 'POST': # If the form has been submitted
        form = AuctionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_price = form.cleaned_data["start_price"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]

            category = Category.objects.get(pk=category)


            auction = Auction(
                publisher = User.objects.get(pk=request.user.id),
                title = title,
                description = description,
                start_price = start_price,
                category = category,
                image = image
            )
            auction.save()

            return render(request, "auctions/item.html",{
                "item": auction
            })
        
        return render(request, "auctions/create_list.html",{
            'form': auction_form
        })

    else:

        return render(request, "auctions/create_list.html",{
            'form': auction_form
        })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def category(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all()
        })

def category_list(request,id):
    items = Auction.objects.filter(category=id)
    return render(request, "auctions/index.html", {
        "active_listings": items
    })
