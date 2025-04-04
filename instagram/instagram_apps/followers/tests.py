from django.test import TestCase
from django.core.exceptions import ValidationError
from instagram_apps.users.models import CustomUser
from instagram_apps.posts.models import Post
from instagram_apps.stories.models import Story
from instagram_apps.interactions.models import Comment, Like  

class CommentLikeModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='pass')
        self.post = Post.objects.create(user=self.user, caption='Post caption')
        self.story = Story.objects.create(user=self.user, caption='Story caption')
    
    # =============== COMMENT TESTS =================

    def test_comment_must_have_post_or_story(self):
        comment = Comment(user=self.user, text='No target')
        with self.assertRaises(ValidationError):
            comment.full_clean()

    def test_comment_on_post_valid(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Nice post!')
        self.assertEqual(comment.post, self.post)

    def test_comment_on_story_valid(self):
        comment = Comment.objects.create(user=self.user, story=self.story, text='Nice story!')
        self.assertEqual(comment.story, self.story)

    def test_comment_str_post(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Wow')
        self.assertIn('wrote Wow comment to this post', str(comment))

    def test_comment_str_story(self):
        comment = Comment.objects.create(user=self.user, story=self.story, text='Hello!')
        self.assertIn('wrote Hello! comment to this story', str(comment))

    def test_comment_created_at_auto(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Check time')
        self.assertIsNotNone(comment.created_at)

    def test_reverse_user_comments(self):
        Comment.objects.create(user=self.user, post=self.post, text='Comment 1')
        self.assertEqual(self.user.comment_set.count(), 1)

    # =============== LIKE TESTS =================

    def test_like_must_have_post_story_or_comment(self):
        like = Like(user=self.user)
        with self.assertRaises(ValidationError):
            like.full_clean()

    def test_like_on_post_valid(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.post, self.post)

    def test_like_on_story_valid(self):
        like = Like.objects.create(user=self.user, story=self.story)
        self.assertEqual(like.story, self.story)

    def test_like_on_comment_valid(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Great!')
        like = Like.objects.create(user=self.user, comment=comment)
        self.assertEqual(like.comment, comment)

    def test_like_str_post(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertIn('liked this post', str(like))

    def test_like_str_story(self):
        like = Like.objects.create(user=self.user, story=self.story)
        self.assertIn('liked this story', str(like))

    def test_like_str_comment(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Good one')
        like = Like.objects.create(user=self.user, comment=comment)
        self.assertIn('liked this comment', str(like))

    def test_like_created_at_auto(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertIsNotNone(like.created_at)

    def test_reverse_user_likes(self):
        Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(self.user.like_set.count(), 1)

    def test_unique_like_on_same_post(self):
        Like.objects.create(user=self.user, post=self.post)
        with self.assertRaises(ValidationError):
            like = Like(user=self.user, post=self.post)
            like.full_clean()

    def test_unique_like_on_same_story(self):
        Like.objects.create(user=self.user, story=self.story)
        with self.assertRaises(ValidationError):
            like = Like(user=self.user, story=self.story)
            like.full_clean()

    def test_unique_like_on_same_comment(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Great!')
        Like.objects.create(user=self.user, comment=comment)
        with self.assertRaises(ValidationError):
            like = Like(user=self.user, comment=comment)
            like.full_clean()

    def test_user_can_like_post_and_story_separately(self):
        Like.objects.create(user=self.user, post=self.post)
        Like.objects.create(user=self.user, story=self.story)
        self.assertEqual(Like.objects.count(), 2)

    def test_user_can_like_comment_and_post_separately(self):
        comment = Comment.objects.create(user=self.user, post=self.post, text='Nice')
        Like.objects.create(user=self.user, post=self.post)
        Like.objects.create(user=self.user, comment=comment)
        self.assertEqual(Like.objects.count(), 2)
