# Generated by Django 5.1.1 on 2024-11-06 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "auctions",
            "0003_rename_item_bid_listing_rename_text_comment_content_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="name",
            new_name="title",
        ),
    ]