from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.utils import timezone

from instagram_apps.users.models import CustomUser
from instagram_apps.posts.models import Post


class PostModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )

    def test_post_created_with_caption(self):
        post = Post.objects.create(user=self.user, caption='Test caption')
        self.assertEqual(post.caption, 'Test caption')
        self.assertEqual(post.user, self.user)

    def test_post_created_with_image(self):
        image = SimpleUploadedFile("image.jpg", b"image_content", content_type="image/jpeg")
        post = Post.objects.create(user=self.user, image=image)
        self.assertTrue(post.image.name.startswith('post_images/'))

    def test_post_created_with_video(self):
        video = SimpleUploadedFile("video.mp4", b"video_content", content_type="video/mp4")
        post = Post.objects.create(user=self.user, video=video)
        self.assertTrue(post.video.name.startswith('post_videos/'))

    def test_post_created_with_all_fields(self):
        image = SimpleUploadedFile("img.jpg", b"x", content_type="image/jpeg")
        video = SimpleUploadedFile("vid.mp4", b"x", content_type="video/mp4")
        post = Post.objects.create(user=self.user, caption="Full", image=image, video=video)
        self.assertEqual(post.caption, "Full")

    def test_post_string_representation(self):
        post = Post.objects.create(user=self.user, caption='Some caption for testing string')
        self.assertTrue(str(post).startswith('testuser: Some caption'))

    def test_post_created_at_auto_now_add(self):
        post = Post.objects.create(user=self.user, caption="Time test")
        self.assertIsNotNone(post.created_at)
        self.assertLessEqual(post.created_at, timezone.now())

    def test_post_default_likes_and_views(self):
        post = Post.objects.create(user=self.user, caption="New post")
        self.assertEqual(post.like_count, 0)
        self.assertEqual(post.views, 0)

    def test_post_ordering(self):
        Post.objects.create(user=self.user, caption="First")
        Post.objects.create(user=self.user, caption="Second")
        posts = Post.objects.all()
        self.assertEqual(posts[0].caption, "Second")
        self.assertEqual(posts[1].caption, "First")

    def test_post_without_any_content_should_fail(self):
        post = Post(user=self.user)
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_post_save_calls_clean(self):
        post = Post(user=self.user)
        with self.assertRaises(ValidationError):
            post.save()

    def test_post_with_only_whitespace_caption_should_fail(self):
        post = Post(user=self.user, caption='   ')
        with self.assertRaises(ValidationError):
            post.full_clean()