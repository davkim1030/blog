from django.contrib.auth.models import User
from django.shortcuts import render
from django.test import TestCase
from django.urls import reverse

from post import views
from post.models import Post


class TestPost(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test_user_1', email='test_user_1', password='password1')
        self.post = Post.objects.create(title='post test 1', author=self.user, content='This is content of tes post 1')

    def tearDown(self) -> None:
        User.objects.filter(id=self.user.id).delete()

    def test_get_post_detail(self):
        # When: calling existing post id
        actual_response = self.client.get(reverse(views.detail, kwargs={'post_id': self.post.id}))

        # Then: returns proper response
        post = Post.objects.get(id=self.post.id)
        values = post.__dict__
        values['author'] = post.author.username
        self.assertEqual(actual_response.content, render(None, 'post/post_detail.html', values).content)

    def test_get_post_detail_not_existing(self):
        # When: calling not existing post id
        actual_response = self.client.get(reverse(views.detail, kwargs={'post_id': 0}))

        # Then: gets 404 not found
        self.assertEqual(actual_response.status_code, 404)

    def test_get_posts_write_when_logged_out(self):
        # When: calling GET /posts/ when logged out
        actual_response = self.client.get(reverse(views.write))

        # Then: gets forbidden
        self.assertEquals(actual_response.status_code, 403)

    def test_get_posts_write_when_logged_in(self):
        # When: calling GET /posts/ when logged in
        actual_response = self.client.get(reverse(views.write))

        # Then: gets posts writting page
        self.assertEquals(actual_response.content, render(None, 'post/post_write.html').content)
