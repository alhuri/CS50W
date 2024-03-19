from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Auction, watchList, Bid, Comment
from django.views.generic import CreateView
from django import forms
from django.forms import formset_factory
from django.shortcuts import get_object_or_404


CHOICES = Category.objects.values_list()

class AuctionForm(forms.Form):
    title = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'style': 'height: 40px; width: 500px;' ,'class': 'form-control'}))
    category = forms.ChoiceField(choices = CHOICES, widget=forms.Select(attrs={'style': 'height: 40px; width: 500px;' ,'class': 'form-control'}))
    start_price = forms.DecimalField(max_digits=8, widget=forms.NumberInput(attrs={'style': 'height: 40px; width: 500px;' ,'class': 'form-control'}))
    image = forms.URLField(label="Image URL", required=False , widget=forms.TextInput(attrs={'style': 'height: 40px; width: 500px;' ,'class': 'form-control'}))
    description = forms.CharField(max_length=32, widget=forms.Textarea(attrs={'style': 'height: 100px; width: 500px; margin-bottom: 10px;' ,'class': 'form-control'}))

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=255, widget= forms.TextInput
    (attrs={'placeholder':'comment', 'style': 'height: 100px; width: 500px; margin: 10px;','class': 'form-control'}),
    label='')

class BidForm(forms.Form):
    bid = forms.DecimalField(
    widget= forms.TextInput
    (attrs={'placeholder':'bid','style':'margin-bottom:2px;'}),
    label='')

comment_form = CommentForm()
auction_form = AuctionForm()
bid_form = BidForm()

def index(request):
    active = Auction.objects.filter(status=True)
    return render(request, "auctions/index.html",{
        "active_listings": active
        })

def place_bid(request,auction_id):
    if request.method == 'POST': # If the form has been submitted
        form = BidForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            bid = form.cleaned_data["bid"]

            auction = Auction.objects.get(pk=auction_id)
            comments = Comment.objects.filter(auction=auction)
            highest_bid = Bid.objects.filter(auction=auction_id).order_by('-bid').first()

            if bid < highest_bid.bid or bid < auction.start_price: 
                return render(request, "auctions/error.html",{
                    "msg": "The bid Is lower the the last bid!"
                    })
            else:
                new_bid = Bid(
                        bidder = User.objects.get(pk=request.user.id),
                        bid = bid,
                        auction = auction
                        )
                new_bid.save()
                highest_bid = Bid.objects.filter(auction=auction_id).order_by('-bid').first()

                return render(request, "auctions/item.html",{
                    'item': auction,
                    'bid' : highest_bid.bid,
                    'comments' : comments,
                    'bid_form' : BidForm(),
                    'comment_form' : comment_form
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

def item(request,auction_id):
    auction = Auction.objects.get(pk=auction_id)

    if auction.status == False:
        highest_bid = Bid.objects.filter(auction=auction_id).order_by('-bid').first()
        return render(request, "auctions/close.html",{
        'item': auction,
        'bid' : highest_bid,
        })

    else:
        comments = Comment.objects.filter(auction=auction)
        highest_bid = Bid.objects.filter(auction=auction_id).order_by('-bid').first()

        return render(request, "auctions/item.html",{
            'item': auction,
            'bid' : highest_bid.bid,
            'comments' : comments,
            'bid_form' : BidForm(),
            'comment_form' : comment_form
            })

def close(request,auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.status= False
    auction.save()
    highest_bid = Bid.objects.filter(auction=auction_id).order_by('-bid').first()


    return render(request, "auctions/close.html",{
        'item': auction,
        'bid' : highest_bid,
        })

def create_list(request):
    return render(request, "auctions/create_list.html",{
        'form': auction_form
    })

def watch_list(request, id):
    auction = Auction.objects.get(pk=id)
    if watchList.objects.filter(watcher = request.user.id, auction = auction).exists():
        return render(request, "auctions/error.html",{
                "msg": "Product Already Added!"
            })

    else:
        watchlist = watchList(
                watcher = User.objects.get(pk=request.user.id),
                auction = auction
            )
        watchlist.save()

        return render(request, "auctions/watch_listing.html",{
                "active_listings": watchList.objects.filter(watcher_id=request.user.id)
            })

def remove_item_watch_list(request, auction):
    watchlist = watchList.objects.filter(watcher=request.user.id, auction=auction)
    watchlist.delete()
    return render(request, "auctions/watch_listing.html",{
            "active_listings": watchList.objects.filter(watcher_id=request.user.id)
        })

def watch_listing(request):
    watch = watchList.objects.filter(watcher_id=request.user.id)
    if watch != None:
        return render(request, "auctions/watch_listing.html",{
                "active_listings": watch
            })
    else:
        return render(request, "auctions/error.html",{
                "msg": "Empty!"
            })

def comment(request, auction_id):
    if request.method == 'POST': # If the form has been submitted
        form = CommentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            comment = form.cleaned_data["comment"]

            comment = Comment(
                commentor = User.objects.get(pk=request.user.id),
                content = comment,
                auction = Auction.objects.get(pk=auction_id)
            )
            comment.save()

            auction = Auction.objects.get(pk=auction_id)
            comments = Comment.objects.filter(auction=auction)
            highest_bid = Bid.objects.filter(auction=auction_id).order_by('-bid').first()


            return render(request, "auctions/item.html",{
                'item': auction,
                'bid' : highest_bid.bid,
                'comments' : comments,
                'bid_form' : BidForm(),
                'comment_form' : comment_form
                })

    else:

        return render(request, "auctions/item.html",{
                'item': auction,
                'bid' : highest_bid.bid,
                'comments' : comments,
                'bid_form' : BidForm(),
                'comment_form' : comment_form
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
            bid = form.cleaned_data["start_price"]
            bidder = User.objects.get(pk=request.user.id)

            if image == None:
                image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTelVna9__Qwt9GifGdE0R4FmsiTmZjoSE1vnC4LXdgozvqbjiOGufuXrladHL7nXowTt4&usqp=CAU"

            category = Category.objects.get(pk=category)


            auction_object = Auction(
                publisher = User.objects.get(pk=request.user.id),
                title = title,
                description = description,
                start_price = start_price,
                category = category,
                image = image
            )
            auction_object.save()

            bid_object = bid(
                bidder = bidder,
                bid = bid
            )
            bid_object.save()

            auction = Auction.objects.get(pk=auction_object.id)
            comments = Comment.objects.filter(auction=auction_object)
            highest_bid = Bid.objects.filter(auction=auction_object.id).order_by('-bid').first()

            return render(request, "auctions/item.html",{
                'item': auction,
                'bid' : highest_bid.bid,
                'comments' : comments,
                'bid_form' : BidForm(),
                'comment_form' : comment_form
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
