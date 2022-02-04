from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Название группы'
    )
    slug = models.SlugField('Адрес', unique=True, help_text='Адрес группы')
    description = models.TextField(
        'Описание', help_text='Описание группы')

    class Meta:
        verbose_name = 'Группа'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Текст', help_text='Текст поста')
    pub_date = models.DateTimeField('Дата пуликации',
                                    help_text='Дата публикации поста',
                                    auto_now_add=True,)
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        help_text='Связанная группа'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return (self.text[:15])
