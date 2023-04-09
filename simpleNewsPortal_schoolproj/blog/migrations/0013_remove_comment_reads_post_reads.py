# Generated by Django 4.1.7 on 2023-03-13 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0012_comment_reads"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="reads",
        ),
        migrations.AddField(
            model_name="post",
            name="reads",
            field=models.IntegerField(default=0),
        ),
    ]