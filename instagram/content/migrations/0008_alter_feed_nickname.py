# Generated by Django 4.1.9 on 2023-06-13 07:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0007_alter_feed_nickname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feed",
            name="nickname",
            field=models.TextField(default="", max_length=24, unique=True),
        ),
    ]
