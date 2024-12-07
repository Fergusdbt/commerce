from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment
import math


def index(request):
    listings = Listing.objects.filter(sold=False)
    return render(request, "auctions/index.html", {
        "listings": listings
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

@login_required
def new(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        image = request.POST["image"]
        category = request.POST["category"]
        user = User.objects.get(username=request.user.username)

        try:
            listing = Listing(title=title, description=description, starting_price=starting_price, current_bid="0.00", image=image, category=category, user=user, highest_bidder=user)
            listing.save()

        except IntegrityError:
            return render(request, "auctions/new.html", {
                "message": "Unknown error"
            })

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/new.html")


def listing(request, title):
    if request.method=="POST":

        if request.POST["button"] == "Add to watchlist":
            user = User.objects.get(username=request.user.username)
            listing = Listing.objects.get(title=title)
            listing.watchers.add(user)
            listing.save()
            user.watch_count += 1
            user.save()
            return render(request, "auctions/listing.html", {
                "listing": listing
            })

        if request.POST["button"] == "Remove from watchlist":
            user = User.objects.get(username=request.user.username)
            listing = Listing.objects.get(title=title)
            listing.watchers.remove(user)
            listing.save()
            user.watch_count -= 1
            user.save()
            return render(request, "auctions/listing.html", {
                "listing": listing
            })

        if request.POST["button"] == "Place Bid":
            user = User.objects.get(username=request.user.username)
            listing = Listing.objects.get(title=title)
            starting_price = listing.starting_price
            current_bid = listing.current_bid
            amount = float(request.POST["bid"])

            if current_bid == 0.00:

                if amount < starting_price and not math.isclose(amount, starting_price, abs_tol=1e-9):
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "message": "Bid must be equal or more than the starting price."
                    })

                else:
                    try:
                        bid = Bid(listing=listing, user=user, amount=amount, winning=True)
                        bid.save()

                        listing.highest_bidder = user
                        listing.current_bid = amount
                        listing.bid_count += 1
                        listing.save()

                    except IntegrityError:
                        return render(request, "auctions/listing.html", {
                            "message": "Unknown error"
                        })
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "message": "Your bid was successful."
                    })

            else:
                if amount <= current_bid or math.isclose(amount, current_bid, abs_tol=1e-9):
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "message": "Bid must be more than the current price."
                    })

                else:
                    try:
                        previous_bid = Bid.objects.get(winning=True)
                        previous_bid.winning = False
                        previous_bid.save()

                        bid = Bid(listing=listing, user=user, amount=amount, winning=True)
                        bid.save()

                        listing.highest_bidder = user
                        listing.current_bid = amount
                        listing.bid_count += 1
                        listing.save()

                    except IntegrityError:
                        return render(request, "auctions/listing.html", {
                            "message": "Unknown error"
                        })
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "message": "Your bid was successful."
                    })

        if request.POST["button"] == "Close auction":
            user = User.objects.get(username=request.user.username)
            listing = Listing.objects.get(title=title)
            listing.sold = True
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing
            })

        if request.POST["button"] == "Comment":
            user = User.objects.get(username=request.user.username)
            listing = Listing.objects.get(title=title)
            content = request.POST["comment"]
            comment = Comment(listing=listing, user=user, content=content)
            comment.save()
            return render(request, "auctions/listing.html", {
                "listing": listing
            })

    else:
        listing = Listing.objects.get(title=title)
        return render(request, "auctions/listing.html", {
            "listing": listing
        })


@login_required
def watchlist(request, username):
    user = User.objects.get(username=username)
    watchlist = Listing.objects.filter(watchers=user.id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


def categories(request):
        categories = [choice[1] for choice in Listing._meta.get_field('category').choices]
        return render(request, "auctions/categories.html", {
            "categories": categories
        })


def category(request, category):
    listings = Listing.objects.filter(category=category.lower(), sold=False)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })
