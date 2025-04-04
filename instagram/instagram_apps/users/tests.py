from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .serializers import CustomUserSerializer
from django.contrib.auth.hashers import check_password


User = get_user_model()

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123456789'
        )

    def test_user_created_correctly(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')

    def test_password_is_hashed(self):
        raw_password = 'TestPass123456789'
        self.assertTrue(check_password(raw_password, self.user.password))

    def test_username_uniqueness(self):
        with self.assertRaises(Exception):
            User.objects.create_user(username='testuser', email='another@example.com', password='AnotherPass123')

    def test_email_uniqueness(self):
        with self.assertRaises(Exception):
            User.objects.create_user(username='newuser', email='test@example.com', password='AnotherPass123')

    def test_default_profile_status(self):
        self.assertEqual(self.user.profile_status, User.OPEN_PROFILE)

    def test_profile_status_change(self):
        self.user.profile_status = User.PRIVATE_PROFILE
        self.user.save()
        self.assertEqual(self.user.profile_status, User.PRIVATE_PROFILE)

    def test_bio_field_update(self):
        bio = "My bio info."
        self.user.bio = bio
        self.user.save()
        self.assertEqual(self.user.bio, bio)

    def test_bio_max_length(self):
        bio = "a" * 155
        self.user.bio = bio
        self.user.save()
        self.assertEqual(len(self.user.bio), 155)

    def test_profile_picture_upload(self):
        image = SimpleUploadedFile(name='test.jpg', content=b'image_content', content_type='image/jpeg')
        self.user.profile_picture = image
        self.user.save()
        self.assertTrue(self.user.profile_picture.name.startswith('profile/pictures'))

    def test_profile_picture_null(self):
        self.assertIsNone(bool(self.user.profile_picture))

    def test_followers_followings_default_count(self):
        self.assertEqual(self.user.followers_count, 0)
        self.assertEqual(self.user.followings_count, 0)

    def test_str_representation(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_serializer_fields_exist(self):
        serializer = CustomUserSerializer(self.user)
        data = serializer.data
        self.assertIn('username', data)
        self.assertIn('email', data)
        self.assertIn('profile_status', data)
        self.assertIn('bio', data)

    def test_create_user_with_serializer(self):
        data = {
            'username': 'serializeruser',
            'email': 'serializer@example.com',
            'password': 'StrongPass123!',
            'profile_status': User.PRIVATE_PROFILE,
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'serializeruser')
        self.assertEqual(user.email, 'serializer@example.com')

    def test_password_validation_success(self):
        try:
            validate_password('ValidPass123456789!')
        except ValidationError:
            self.fail("Password validation unexpectedly failed.")

    def test_password_validation_fail(self):
        with self.assertRaises(ValidationError):
            validate_password('123')

    def test_user_login_success(self):
        login = self.client.login(username='testuser', password='TestPass123456789')
        self.assertTrue(login)

    def test_user_login_fail(self):
        login = self.client.login(username='testuser', password='WrongPass')
        self.assertFalse(login)

    def test_user_list_authenticated(self):
        User.objects.create_user(username='user2', email='u2@example.com', password='pass')
        self.client.force_authenticate(user=self.user)
        url = reverse('customuser-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_user_list_unauthenticated(self):
        url = reverse('customuser-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [401, 403])

    def test_user_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('customuser-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_update_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('customuser-detail', args=[self.user.id])
        response = self.client.patch(url, {"bio": "Updated bio."}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['bio'], "Updated bio.")