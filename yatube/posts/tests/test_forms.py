import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.form = PostForm()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testgroup',
            description='Описание группы',
        )
        cls.new_group = Group.objects.create(
            title='Новая тестовая группа',
            slug='newtestgroup',
            description='Описание новой группы',
        )
        cls.post = Post.objects.create(
            text='Test text',
            author=cls.user,
            group=cls.group,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.guest_client = Client()
        self.authorized_client.force_login(PostFormTest.user)

    def test_edit_post(self):
        post_id = PostFormTest.post.id
        post_data = {
            'text': 'New test text',
            'group': PostFormTest.new_group.id,
        }
        kwargs_post = {
            'post_id': post_id,
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs=kwargs_post),
            data=post_data,
            follow=True,
        )

        self.assertRedirects(response,
                             reverse('posts:post_detail', kwargs=kwargs_post))
        self.assertEqual(Post.objects.get(id=post_id).text, post_data['text'])
        self.assertEqual(Post.objects.get(id=post_id).group.id,
                         post_data['group'])


class CommentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='Тестовый автор')
        cls.user = User.objects.create(username='Тестовый пользователь')
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый текст',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(CommentTest.user)
        self.form_data = {'post': 'Тестовый комментарий'}

    def unauthorized_user_cant_comment(self):
        response = self.guest_client.post(reverse(
            'add_comment', args=[CommentTest.author.username,
                                 CommentTest.post.id]))
        self.assertRedirects(response, reverse(
            'post', args=[CommentTest.author.username,
                          CommentTest.post.id]))

    def authorized_user_can_comment(self):
        self.authorized_client.post(reverse(
            'add_comment',
            args=[CommentTest.author.username, CommentTest.post.id]),
            data=self.form_data, follow=True)
