# Generated by Django 3.2.16 on 2022-10-19 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="category",
        ),
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="blog.category",
            ),
        ),
    ]
