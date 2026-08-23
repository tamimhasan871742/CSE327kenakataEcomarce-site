from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestLoginView(TestCase):

    def setUp(self):
        # Create normal user
        self.user = User.objects.create_user(
            email="user@example.com",
            username="testuser",
            password="testpass"
        )

        # Create staff user (admin)
        self.admin = User.objects.create_user(
            email="admin@example.com",
            username="adminuser",
            password="adminpass",
            is_staff=True
        )

        # Create superuser
        self.superuser = User.objects.create_superuser(
            email="super@example.com",
            username="superuser",
            password="superpass"
        )

        self.client = Client()

    
    def test_login_view_success(self):
        response = self.client.post(reverse("login"), {
            "email": "user@example.com",
            "password": "testpass"
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome back, testuser!")
        user = response.context['user']
        self.assertTrue(user.is_authenticated)

    def test_login_view_admin_blocked(self):
        response = self.client.post(reverse("login"), {
            "email": "adminuser@example.com",
            "password": "adminpass"
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin users cannot log in here.")
        user = response.context['user']
        self.assertFalse(user.is_authenticated)

    
    def test_login_view_invalid_credentials_fail(self):
        response = self.client.post(reverse("login"), {
            "email": "user@example.com",
            "password": "wrongpass"
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password.")
        
        user = response.context['user']
        self.assertTrue(user.is_authenticated)  

    def test_login_view_wrong_email_fail(self):
        response = self.client.post(reverse("login"), {
            "email": "fake@example.com",
            "password": "testpass"
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password.")
       
        self.assertContains(response, "Welcome back, testuser!")  

    def test_login_view_get_request_fail(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
       
        messages = list(response.context.get("messages", []))
        self.assertTrue(messages)  

  
    def test_login_view_empty_email_password(self):
        response = self.client.post(reverse("login"), {
            "email": "",
            "password": ""
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password.")

    def test_login_view_only_email(self):
        response = self.client.post(reverse("login"), {
            "email": "user@example.com",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password.")

    def test_login_view_only_password(self):
        response = self.client.post(reverse("login"), {
            "password": "testpass",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password.")

    def test_login_view_superuser_blocked(self):
        response = self.client.post(reverse("login"), {
            "email": "super@example.com",
            "password": "superpass"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin users cannot log in here.")
        user = response.context['user']
        self.assertFalse(user.is_authenticated)

    
    def test_login_view_wrong_template_fail(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "wrong_template.html")  
