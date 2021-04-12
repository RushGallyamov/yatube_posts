from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class Group(models.Model):
    """Класс, описивающий структуру сообщества"""
    title = models.CharField(
        'Название сообщества',
        max_length=200,
        help_text='Дайте короткое название сообществу'
    )
    slug = models.SlugField(
        'Адрес',
        max_length=200,
        unique=True
    )
    description = models.TextField(
        'Описание сообщества',
        max_length=700,
        blank=True, null=True,
        help_text='Дайте короткое описание сообществу'
    )

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Класс, описивающий структуру поста"""
    text = models.TextField(
        verbose_name='Текст',
        max_length=700,
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Сообщество'
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True, null=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Класс, описивающий структуру комментария"""
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=700,
        help_text='Введите текст комментария'
    )
    created = models.DateTimeField(
        'Дата создания комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created']

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='following',
    )
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='follower',
    )
