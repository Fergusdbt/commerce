# Generated by Django 5.1.1 on 2024-12-06 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0017_user_watch_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="sold",
            field=models.BooleanField(default=False),
        ),
    ]
