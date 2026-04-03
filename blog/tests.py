from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import CustomUser

from .models import Post


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class BlogWorkflowTests(TestCase):
    def setUp(self):
        self.password = "StrongPass123!"
        self.user = CustomUser.objects.create_user(phone="09123456789", password=self.password)
        self.admin = CustomUser.objects.create_superuser(phone="09999999999", password=self.password)
        self.post = Post.objects.create(
            title="Trade Notes",
            author=self.admin,
            summary="Short summary",
            body="Full body",
        )

    def test_blog_pages_render_publicly(self):
        self.assertEqual(self.client.get(reverse("Blog")).status_code, 200)
        self.assertEqual(self.client.get(reverse("PostDetails", args=[self.post.id])).status_code, 200)

    def test_blog_admin_write_paths_require_superuser(self):
        self.client.force_login(self.user)

        for url in [
            reverse("PostCreate"),
            reverse("PostEdit", args=[self.post.id]),
            reverse("PostDelete", args=[self.post.id]),
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("PostCreate")).status_code, 200)

    def test_admin_can_create_post_and_author_is_request_user(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("PostCreate"),
            {"title": "New Post", "summary": "Created by admin", "body": "Body copy"},
        )

        created_post = Post.objects.get(title="New Post")
        self.assertRedirects(response, reverse("PostDetails", args=[created_post.id]))
        self.assertEqual(created_post.author, self.admin)
        self.assertEqual(created_post.summary, "Created by admin")
