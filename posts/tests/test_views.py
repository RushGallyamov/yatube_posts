import shutil
import tempfile

from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.test import Client, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Group, Post, Follow

USER = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.test_user = USER.objects.create_user(username='tester')
        cls.authorised_client = Client()
        cls.authorised_client.force_login(cls.test_user)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.group = Group.objects.create(
            id=1,
            title='Тестовое сообщество',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст поста',
            author=cls.test_user,
            image=cls.uploaded,
            group_id=1
        )
        cls.reversed_pages = {
            'group.html': reverse('group', kwargs={'slug': 'test-slug'}),
            'index.html': reverse('index'),
            'post_form.html': reverse('new_post')
        }
        cls.expected_post_fields = {
            'text': forms.CharField
        }
        cls.expected_group_fields = {
            'title': forms.CharField,
            'slug': forms.SlugField
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_pages_use_correct_template(self):
        """Url-адреса используют соответствующие шаблоны"""
        for template, reversed_name in PostPagesTests.reversed_pages.items():
            with self.subTest(reversed_name=reversed_name):
                response = self.authorised_client.get(reversed_name)
                self.assertTemplateUsed(response, template)

    def test_newpost_page_shows_correct_context(self):
        """Context new_post сформирован верно"""
        response = PostPagesTests.authorised_client.get(reverse('new_post'))
        for value, expected in PostPagesTests.expected_post_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_home_page_shows_correct_context(self):
        """
        Context главной страницы сформирован верно,
        посты появляются на главной странице
        """
        response = PostPagesTests.authorised_client.get(reverse('index'))
        post = PostPagesTests.post
        response_post = response.context.get('page')[0]
        self.assertEqual(post, response_post)

    def test_group_page_shows_correct_context(self):
        """
        Context страницы сообщества сформирован верно,
        посты появляются на странице группы
        """
        post = PostPagesTests.post
        group = PostPagesTests.group
        response = PostPagesTests.authorised_client.get(
            reverse(
                'group', kwargs={'slug': group.slug}))
        response_post_from_group = response.context.get('page')[0]
        self.assertEqual(post, response_post_from_group)

    def test_image_file_is_in_context(self):
        """Context страниц содержит загруженное изображение"""
        user = PostPagesTests.test_user
        post = PostPagesTests.post
        urls = {
            reverse('index'): 'page',
            reverse('group', kwargs={'slug': 'test-slug'}): 'page',
            reverse('profile', kwargs={'username': user.username}): 'page',
        }
        for url, context_name in urls.items():
            with self.subTest(url=url):
                response = self.authorised_client.get(url)
                self.assertTrue(response.context[context_name][0].image)

        post_response = self.authorised_client.get(reverse(
            'post',
            kwargs={'username': user.username, 'post_id': post.id}))
        self.assertTrue(post_response.context['post'].image)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = USER.objects.create_user(username='tester')
        cls.authorised_client = Client()
        cls.authorised_client.force_login(cls.test_user)
        for i in range(13):
            Post.objects.create(
                text=f'Тестовый текст поста {i}',
                author=cls.test_user
            )

    def test_first_page_containse_ten_records(self):
        """Первая страница содержит 10 постов"""
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        """Вторая страница содержит 3 поста"""
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)


class CachTests(TestCase):

    def test_index_cached_correctly(self):
        """Главная страница кэшируется"""
        user_client = Client()
        test_user = USER.objects.create_user(username='tester')
        response_before = user_client.get(reverse('index'))
        Post.objects.create(
            text='Текст',
            author=test_user
        )
        response_after = user_client.get(reverse('index'))
        self.assertEqual(response_before.content, response_after.content)


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.follower = USER.objects.create_user(username='follower')
        cls.follower_client = Client()
        cls.follower_client.force_login(cls.follower)
        cls.followed = USER.objects.create_user(username='followed')
        cls.followed_client = Client()
        cls.followed_client.force_login(cls.followed)
        cls.unsubscribed = USER.objects.create_user(username='unsubscribed')
        cls.unsubscribed_client = Client()
        cls.unsubscribed_client.force_login(cls.unsubscribed)
        cls.post = Post.objects.create(
            text='Тестовый текст поста',
            author=cls.followed,
        )

    def test_authorised_user_able_to_subscribe(self):
        """Авторизированный пользователь может подписываться"""
        count_before = Follow.objects.count()
        FollowTests.follower_client.get(reverse(
            'profile_follow',
            kwargs={
                "username": FollowTests.followed.username
            }
        ))
        count_after = Follow.objects.all().count()
        self.assertEqual(count_before + 1, count_after)

    def test_authorised_user_able_to_unsubscribe(self):
        """Авторизированный пользователь может отписываться"""
        follower = FollowTests.follower
        followed = FollowTests.followed
        Follow.objects.create(user=follower, author=followed)
        count_before = Follow.objects.count()
        FollowTests.follower_client.get(reverse(
            'profile_unfollow',
            kwargs={
                "username": FollowTests.followed.username
            }
        ))
        count_after = Follow.objects.all().count()
        self.assertEqual(count_before, count_after + 1)

    def test_follow_index_shows_correct_posts(self):
        """
        Новая запись пользователя появляется в ленте тех, кто на него подписан
        """
        follower = FollowTests.follower_client
        follower.get(reverse(
            'profile_follow',
            kwargs={
                "username": FollowTests.followed.username
            }
        ))
        response_follower = follower.get(reverse('follow_index'))
        self.assertEqual(
            response_follower.context.get('page')[0], FollowTests.post
        )

    def test_follow_index_shows_correct_posts(self):
        """
        Новая запись пользователя не появляется в ленте тех,
        кто на него не подписан
        """
        unsubscribed = FollowTests.unsubscribed_client
        response_unsubscribed = unsubscribed.get(reverse('follow_index'))
        self.assertFalse(response_unsubscribed.context['posts'])
