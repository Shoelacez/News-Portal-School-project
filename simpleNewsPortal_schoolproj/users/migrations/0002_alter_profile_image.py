# Generated by Django 4.1.7 on 2023-03-10 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="profile_pics"),
        ),
    ]
