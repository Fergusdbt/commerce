from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watch_count = models.IntegerField(default=0)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_price = models.DecimalField(max_digits=5 , decimal_places=2)
    current_bid = models.DecimalField(max_digits=5 , decimal_places=2)
    image = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=64, choices=[
        ("Electronics", "Electronics"),
        ("Fashion", "Fashion"),
        ("Home", "Home"),
        ("Toys", "Toys"),
        ("Other", "Other")
    ], blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date_posted = models.DateTimeField(auto_now_add=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    bid_count = models.IntegerField(default=0)
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winning_bids")
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"Listing {self.id}: {self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    date_posted = models.DateTimeField(auto_now_add=True)
    winning = models.BooleanField(default=False)

    def __str__(self):
        return f"Bid {self.id} by {self.user} on Listing {self.listing.id}: {self.listing.title}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} by {self.user} on Listing {self.listing.id}: {self.listing.title}"
