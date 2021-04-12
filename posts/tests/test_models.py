from django.test import TestCase
from posts.models import Post, Group
from django.contrib.auth import get_user_model

USER = get_user_model()


class GroupModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model_group = Group.objects.create(
            title='Название тестового сообщества больше 15 символов',
        )

    def verbose_name(self):
        """verbose_name group совпадает с ожидаемым"""
        model = GroupModelTests.model_group
        expected_verboses = {
            'title': 'Название сообщества',
            'slug': 'Адрес',
            'description': 'Описание сообщества',
        }
        for value, expected in expected_verboses.items():
            with self.subTest(value=value):
                self.assertEquals(
                    model._meta.get_field(value).verbose_name, expected)

    def help_text(self):
        """help text group совпадает с ожидаемым"""
        model = GroupModelTests.model_group
        expected_helps = {
            'title': 'Дайте короткое название сообществу',
            'description': 'Дайте короткое описание сообществу',
        }
        for value, expected in expected_helps.items():
            with self.subTest(value=value):
                self.assertEquals(
                    model._meta.get_field(value).help_text, expected)

    def test_str_method(self):
        """
        __str__ group это строка с содержимым group.title
        """
        model = GroupModelTests.model_group
        expected_title = model.title
        self.assertEquals(expected_title, str(model))


class PostModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = USER.objects.create(
            username='test_user'
        )
        cls.model_post = Post.objects.create(
            text='Текст тестового поста',
            author=cls.test_user
        )

    def verbose_name(self):
        """verbose_name post совпадает с ожидаемым"""
        model = PostModelTests.model_post
        expected_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Сообщество'
        }
        for value, expected in expected_verboses.items():
            with self.subTest(value=value):
                self.assertEquals(
                    model._meta.get_field(value).verbose_name, expected
                )

    def help_text(self):
        """help text post совпадает с ожидаемым"""
        model = PostModelTests.model_post
        expected_helps = {
            'text': 'Введите текст поста',
        }
        for value, expected in expected_helps.items():
            with self.subTest(value=value):
                self.assertEquals(
                    model._meta.get_field(value).help_text, expected
                )

    def test_str_method(self):
        """
        __str__ post это строка с содержимым post.text
        длиной не больше 15 символов
        """
        model = PostModelTests.model_post
        expected_title = model.text[:15]
        self.assertEquals(expected_title, str(model))
