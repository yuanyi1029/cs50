from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def create(request):
    if request.method == "POST":
        user = request.user
        item = request.POST["item"]
        desc = request.POST["description"]
        price = float(request.POST["price"])
        category = request.POST["category"]
        image_url = request.POST["image_url"]
        time = datetime.now()

        listing = Listing(owner=user, item=item, desc=desc, price=price, image_url=image_url, category=category, active=True, time=time)
        listing.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html")

def watchlist(request):
    user = request.user

    if request.method == "POST":
        listing_id = int(request.POST["watchlist"].split(" ")[2])
        listing = Listing.objects.get(pk=listing_id)
        user.watchlist.add(listing)

        return render(request, "auctions/watchlist.html",{
            "watchlist": user.watchlist.all()
        })

    else:
        return render(request, "auctions/watchlist.html", {
            "watchlist": user.watchlist.all()
        })

def remove(request):
    user = request.user

    if request.method == "POST":
        listing_id = int(request.POST["remove_item"].split(" ")[2])
        listing = Listing.objects.get(pk=listing_id)
        user.watchlist.remove(listing)
        
        return render(request, "auctions/watchlist.html", {
            "watchlist": user.watchlist.all()
        })

    else:
        return HttpResponseRedirect(reverse("index"))


def categories(request):
    if request.method == "POST":
        category = request.POST["category"]
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/categories.html", {
            "listings": listings
        })
    else:
        return render(request, "auctions/categories.html")

def view_listing(request, listing_id):
    listing_item = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(comment_item=listing_item)
    bidder = request.user
    current_winner = Bid.objects.filter(bid_item=listing_item).order_by('-amount')[0].bidder

    if request.method == "POST":
        amount = int(request.POST["amount"])
        time = datetime.now()

        if amount <= listing_item.price:
            return render(request, "auctions/listings.html", {
                "listing": listing_item,
                "comments": comments,
                "message": "Bid cannot be lower than the price!",
                "current_winner": current_winner
            })

        else:
            bid = Bid(bidder=bidder, bid_item=listing_item, amount=amount, time=time) 
            listing_item.price = amount
            listing_item.save()
            bid.save()

            return render(request, "auctions/listings.html", {
                "listing": listing_item,
                "comments": comments,
                "current_winner": current_winner
            })

    else:
        listing_item = Listing.objects.get(pk=listing_id)

        return render(request, "auctions/listings.html", {
            "listing": listing_item,
            "comments": comments,
            "current_winner": current_winner
        })


def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))


def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        content = request.POST["comment"]
        time = datetime.now()
        comment = Comment(commenter=request.user, comment_item=listing, comment=content, time=time)
        comment.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("index"))

