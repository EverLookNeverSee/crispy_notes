from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
from random import choice, randint


category_list = ["Fun", "Economy", "Design", "Engineering", "Art"]


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.fake = Faker()

    def handle(self, *args, **options):
        for _ in range(5):
            f_name = self.fake.first_name()
            l_name = self.fake.last_name()
            user = User.objects.create_user(email=f"{f_name}.{l_name}@email.com", password="Test@123456")
            profile = Profile.objects.get(user=user)
            profile.first_name = f_name
            profile.last_name = l_name
            profile.bio = self.fake.paragraph(nb_sentences=5)
            profile.save()

            for _ in range(100):
                post = Post.objects.create(
                    author=profile,
                    title=self.fake.paragraph(nb_sentences=1),
                    content=self.fake.paragraph(nb_sentences=85),
                    login_required=choice([True, False]),
                    ok_to_publish=choice([True, False]),
                    publish_date=timezone.now(),
                )
                post.n_views = randint(1, 200)
                category = Category.objects.get(name=choice(category_list)),
                post.category.set(category)
                post.save()
