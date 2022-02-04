from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Post, Group

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


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=TEST_AUTHOR['username']
        )
        cls.user_2 = User.objects.create_user(
            username='SecondUser'
        )
        cls.group = Group.objects.create(
            title=TEST_GROUP['title'],
            slug=TEST_GROUP['slug'],
            description=TEST_GROUP['description']
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def test_models_have_correct_object_names(self):
        post = PostModelTest.post
        group = PostModelTest.group
        expected_names = {
            post: 'Тестовый пост',
            group: TEST_GROUP['title'],
        }
        for model, name in expected_names.items():
            with self.subTest(model=model):
                self.assertEqual(
                    str(model), name,
                    f'В модели {model} некорректно работает метод __str__.'
                )

    def test_models_help_text(self):
        post = PostModelTest.post
        expected_help_texts = {
            post: {
                'text': 'Текст поста',
                'group': 'Связанная группа',
            },
        }
        for model, help_texts in expected_help_texts.items():
            with self.subTest(model=model):
                for field, expected_text in help_texts.items():
                    with self.subTest(field=field):
                        self.assertEqual(
                            model._meta.get_field(field).help_text,
                            expected_text,
                            f'В модели {model} некорректные help_text.'
                        )
