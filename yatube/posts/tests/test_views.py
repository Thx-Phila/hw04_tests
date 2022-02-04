from datetime import timezone
import time
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()

TEST_POST = {
    'text': 'Тестовый пост'
}

TEST_GROUP = {
    'title': 'Тестовая группа',
    'slug': 'test_slug',
    'description': 'Тестовое описание'
}

TEST_AUTHOR = {
    'username': 'Author'
}

TEST_COMMENT = {
    'text': 'Тестовый комментарий'
}


class TaskPagesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Yasha1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='Тест',
            slug='1234567',
        )
        self.post = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
            group=self.group
        )
        self.form_data = {
            'text': 'formtesttext',
            'group': self.group.id,
        }
        self.new_post = self.authorized_client.post(
            reverse('posts:post_create'),
            data=self.form_data,
            follow=True
        )

        self.public_index_template = 'posts/index.html'
        self.public_group_page_template = 'posts/group_list.html'
        self.private_create_post_template = 'posts/create_post.html'
        self.private_edit_post_template = 'posts/create_post.html'
        self.public_profile = 'posts/profile.html'
        self.public_post = 'posts/post_detail.html'


class URLPathTemplatesTests(TestCase):

    def test_right_temlate_use_with_url(self):
        url_template_name = (
            ('/about/author/', 'about/author.html'),
            ('/about/tech/', 'about/tech.html'),
        )

        for page_url, template_name in url_template_name:
            with self.subTest(url=page_url, temlate=template_name):
                response = self.client.get(page_url)
                self.assertTemplateUsed(response, template_name)


class ImageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Yasha1")
        self.client.force_login(self.user)

        self.group = Group.objects.create(title="test",
                                          slug="test123",
                                          description='test')

        self.post_valid_file_type = Post.objects.create(
            text='Test text',
            author=self.user,
            group=self.group,
            image=SimpleUploadedFile(name='test.png',
                                     content=open('test.png', 'rb').read(),
                                     content_type='image/png'),
            pub_date=timezone.now()

        )

        self.post_invalid_file_type = Post.objects.create(
            text='Test text',
            author=self.user,
            group=self.group,
            pub_date=timezone.now()

        )


class Cache(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Yasha',
                                             email='Wade333@list.ru',
                                             password='q421162Q')
        self.client.force_login(self.user)

    def test_cache(self):
        response = self.client.get('/')
        self.text = 'Тест cash'
        self.post = Post.objects.create(text=self.text, author=self.user)
        self.assertNotContains(response, self.text)
        time.sleep(20)
        response = self.client.get('/')
        self.assertContains(response, self.text)
