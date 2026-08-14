from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class TestUserModel(TestCase):

    # ---------- BASIC USER CREATION ----------
    def test_create_user_success(self):
        user = User.objects.create_user(
            email="TestUser@Example.com",
            username="testuser",
            password="mypassword123",
            bio="Hello! I am a test user."
        )

        # Email normalized
        self.assertEqual(user.email, "testuser@example.com")

        # __str__
        self.assertEqual(str(user), "testuser")

        # Password hashing
        self.assertNotEqual(user.password, "mypassword123")
        self.assertTrue(user.check_password("mypassword123"))

        # Flags
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    # ---------- FIELD VALIDATIONS ----------
    def test_email_must_be_unique(self):
        User.objects.create_user(
            email="duplicate@example.com",
            username="one",
            password="pass"
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="duplicate@example.com",
                username="two",
                password="pass"
            )

    def test_email_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                username="nouser",
                password="pass"
            )

    def test_invalid_email(self):
        user = User(
            email="not-an-email",
            username="tester",
            password="pass"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_username_required(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                email="user@example.com",
                password="pass"
            )

    def test_username_max_length(self):
        user = User(
            email="valid@example.com",
            username="x" * 101,
            password="pass"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_bio_max_length(self):
        user = User(
            email="bio@example.com",
            username="bio_user",
            bio="x" * 301,
            password="pass"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    # ---------- EMAIL NORMALIZATION ----------
    def test_email_normalization(self):
        user = User.objects.create_user(
            email="LOWERCASE@DOMAIN.COM",
            username="lowerUser",
            password="pass123"
        )
        self.assertEqual(user.email, "lowercase@domain.com")

    def test_email_not_re_normalized_on_update(self):
        user = User.objects.create_user(
            email="Case@Example.com",
            username="caseuser",
            password="pass123"
        )
        user.username = "updated"
        user.save()
        self.assertEqual(user.email, "case@example.com")
        self.assertEqual(user.username, "updated")

    # ---------- SUPERUSER TESTS ----------
    def test_superuser_creation(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass"
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_superuser_must_have_is_superuser_true(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="badadmin@example.com",
                username="bad",
                password="pass",
                is_superuser=False
            )

    def test_superuser_must_have_is_staff_true(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="badadmin2@example.com",
                username="bad2",
                password="pass",
                is_staff=False
            )

    # ---------- STRING REPRESENTATION ----------
    def test_str_method(self):
        user = User.objects.create_user(
            email="a@a.com",
            username="abc123",
            password="pass"
        )
        self.assertEqual(str(user), "abc123")
