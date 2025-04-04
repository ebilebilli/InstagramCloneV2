from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from instagram_apps.users.models import CustomUser
from instagram_apps.stories.models import Story


class StoryModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='storyuser',
            email='story@example.com',
            password='TestPass123'
        )

    def test_story_created_with_caption(self):
        story = Story.objects.create(user=self.user, caption="Hello story")
        self.assertEqual(story.caption, "Hello story")
        self.assertEqual(story.user, self.user)

    def test_story_created_with_image(self):
        image = SimpleUploadedFile("img.jpg", b"img", content_type="image/jpeg")
        story = Story.objects.create(user=self.user, image=image)
        self.assertTrue(story.image.name.startswith("story_images/"))

    def test_story_created_with_video(self):
        video = SimpleUploadedFile("vid.mp4", b"vid", content_type="video/mp4")
        story = Story.objects.create(user=self.user, video=video)
        self.assertTrue(story.video.name.startswith("story_videos/"))

    def test_story_views_default_zero(self):
        story = Story.objects.create(user=self.user, caption="Views test")
        self.assertEqual(story.views, 0)

    def test_story_ordering(self):
        Story.objects.create(user=self.user, caption="Older")
        Story.objects.create(user=self.user, caption="Newer")
        stories = Story.objects.all()
        self.assertEqual(stories[0].caption, "Newer")

    def test_story_without_any_content_should_fail(self):
        story = Story(user=self.user)
        with self.assertRaises(ValidationError):
            story.full_clean()

    def test_story_with_only_spaces_caption_should_fail(self):
        story = Story(user=self.user, caption="     ")
        with self.assertRaises(ValidationError):
            story.full_clean()

    def test_visible_stories_returns_only_recent(self):
        Story.objects.create(user=self.user, caption="Recent")

        old_story = Story.objects.create(user=self.user, caption="Old")
        old_story.created_at = timezone.now() - timedelta(hours=25)
        old_story.save(update_fields=["created_at"])

        visible = Story.visible_stories()
        self.assertIn("Recent", [s.caption for s in visible])
        self.assertNotIn("Old", [s.caption for s in visible])
        
    def test_str_representation(self):
        story = Story.objects.create(user=self.user, caption="Some test caption")
        self.assertTrue(str(story).startswith("storyuser: Some test"))

    def test_story_save_calls_clean(self):
        story = Story(user=self.user)
        with self.assertRaises(ValidationError):
            story.save()
