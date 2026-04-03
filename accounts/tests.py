from django.test import TestCase, override_settings
from django.urls import reverse

from .models import CustomUser


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class CustomUserTests(TestCase):
    def setUp(self):
        self.password = "StrongPass123!"
        self.user = CustomUser.objects.create_user(phone="09123456789", password=self.password)
        self.other_user = CustomUser.objects.create_user(phone="09123456788", password=self.password)

    def test_create_user_uses_phone_as_login_and_creates_cart(self):
        self.assertEqual(self.user.phone, "09123456789")
        self.assertEqual(self.user.username, "09123456789")
        self.assertTrue(self.user.check_password(self.password))
        self.assertTrue(hasattr(self.user, "cart"))

    def test_signup_view_creates_user_and_cart(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "phone": "09111111111",
                "password1": self.password,
                "password2": self.password,
            },
        )

        self.assertRedirects(response, reverse("login"))
        created_user = CustomUser.objects.get(phone="09111111111")
        self.assertEqual(created_user.username, "09111111111")
        self.assertTrue(hasattr(created_user, "cart"))

    def test_phone_login_redirects_to_homepage(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.phone, "password": self.password},
        )

        self.assertRedirects(response, reverse("HomePage"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.id)

    def test_logout_post_redirects_to_homepage(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("HomePage"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_profile_owner_can_access_but_other_user_gets_forbidden(self):
        self.client.force_login(self.user)

        self.assertEqual(self.client.get(reverse("accounts:profile", args=[self.user.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("accounts:profile-edit", args=[self.user.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("accounts:profile", args=[self.other_user.id])).status_code, 403)
        self.assertEqual(self.client.get(reverse("accounts:profile-edit", args=[self.other_user.id])).status_code, 403)
