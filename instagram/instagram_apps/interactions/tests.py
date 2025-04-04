from django.test import TestCase
from django.core.exceptions import ValidationError

from django.db import IntegrityError
from django.utils import timezone

from instagram_apps.users.models import CustomUser
from instagram_apps.posts.models import Post
from instagram_apps.stories.models import Story
from instagram_apps.interactions.models import Comment, Like


class CommentAndLikeModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(user=self.user, caption="A post")
        self.story = Story.objects.create(user=self.user, caption="A story")

    #comment test
    def test_comment_on_post_success(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text="Nice post!")
        self.assertEqual(comment.post, self.post)
        self.assertIsNone(comment.story)

    def test_comment_on_story_success(self):
        comment = Comment.objects.create(user=self.user, story=self.story, text="Nice story!")
        self.assertEqual(comment.story, self.story)
        self.assertIsNone(comment.post)

    def test_comment_without_post_and_story_should_fail(self):
        comment = Comment(user=self.user, text="No target")
        with self.assertRaises(ValidationError):
            comment.full_clean()

    def test_comment_str_post(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text="Hello")
        self.assertIn("wrote Hello comment to this post", str(comment))

    def test_comment_str_story(self):
        comment = Comment.objects.create(user=self.user, story=self.story, text="Hi")
        self.assertIn("wrote Hi comment to this story", str(comment))

    def test_comment_created_at_auto_now(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text="Timestamp")
        self.assertLessEqual(comment.created_at, timezone.now())

    def test_comment_save_calls_clean(self):
        comment = Comment(user=self.user, text="Invalid")
        with self.assertRaises(ValidationError):
            comment.save()

    #like test

    def test_like_post_success(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.post, self.post)

    def test_like_story_success(self):
        like = Like.objects.create(user=self.user, story=self.story)
        self.assertEqual(like.story, self.story)

    def test_like_comment_success(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text="Yaxşı")
        like = Like.objects.create(user=self.user, comment=comment)
        self.assertEqual(like.comment, comment)

    def test_like_without_any_target_should_fail(self):
        like = Like(user=self.user)
        with self.assertRaises(ValidationError):
            like.full_clean()

    def test_like_post_unique_constraint(self):
        Like.objects.create(user=self.user, post=self.post)
        with self.assertRaises(ValidationError):
            Like.objects.create(user=self.user, post=self.post)

    def test_like_story_unique_constraint(self):
        Like.objects.create(user=self.user, story=self.story)
        with self.assertRaises(ValidationError):
            Like.objects.create(user=self.user, story=self.story)
    
    def test_like_comment_unique_constraint(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text="Test")
        Like.objects.create(user=self.user, comment=comment)
        with self.assertRaises(ValidationError):
            Like.objects.create(user=self.user, comment=comment)

    def test_like_str_post(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertIn("liked this post", str(like))

    def test_like_str_story(self):
        like = Like.objects.create(user=self.user, story=self.story)
        self.assertIn("liked this story", str(like))

    def test_like_str_comment(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text="Text")
        like = Like.objects.create(user=self.user, comment=comment)
        self.assertIn("liked this comment", str(like))

    def test_like_created_at_auto_now(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertLessEqual(like.created_at, timezone.now())
