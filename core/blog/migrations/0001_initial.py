# Generated by Django 3.2.16 on 2022-10-19 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="blog/default.jpg",
                        null=True,
                        upload_to="blog/",
                    ),
                ),
                ("content", models.TextField()),
                ("n_views", models.PositiveIntegerField(default=0)),
                ("ok_to_publish", models.BooleanField(default=False)),
                ("login_required", models.BooleanField(default=False)),
                ("publish_date", models.DateTimeField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.profile",
                    ),
                ),
                ("category", models.ManyToManyField(null=True, to="blog.Category")),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
                "ordering": ["-created_at"],
            },
        ),
    ]
