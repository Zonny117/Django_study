# Generated by Django 4.1.9 on 2023-06-13 02:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0004_bookmark_like_reply"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feed",
            name="like_count",
        ),
    ]
