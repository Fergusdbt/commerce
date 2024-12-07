# Generated by Django 5.1.1 on 2024-12-04 15:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0007_alter_listing_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="watchers",
            field=models.ManyToManyField(
                blank=True, related_name="watchlist", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Electronics", "Electronics"),
                    ("Fashion", "Fashion"),
                    ("Home", "Home"),
                    ("Toys", "Toys"),
                    ("Other", "Other"),
                ],
                max_length=64,
            ),
        ),
    ]
