from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Group, Post
from django.urls import reverse

USER = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовое сообщество',
            slug='test-slug'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = USER.objects.create_user(username='Tester')
        self.authorised_client = Client()
        self.authorised_client.force_login(self.user)
        self.post = Post.objects.create(
            text='Тестовый текст поста',
            author=self.user
        )

    def test_home_url_exists_at_desired_loc(self):
        """
        Главная страница доступна любому пользователю
        """
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_profile_url_exists_at_desired_loc(self):
        """
        Страница профайла доступна любому пользователю
        """
        response = self.guest_client.get(reverse(
            'profile',
            kwargs={'username': self.user.username}
        ))
        self.assertEqual(response.status_code, 200)

    def test_edit_url_exists_at_desired_loc_for_anonymous(self):
        """
        Страница редактирования поста недоступна неавторизованному пользователю
        """
        response = self.guest_client.get(reverse(
            'post_edit',
            kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            }
        ))
        self.assertNotEqual(response.status_code, 200)

    def test_edit_url_exists_at_desired_loc_for_author(self):
        """
        Страница редактирования поста доступна автору
        """
        response = self.authorised_client.get(reverse(
            'post_edit',
            kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            }
        ))
        self.assertEqual(response.status_code, 200)

    def test_edit_url_exists_at_desired_loc_for_author(self):
        """
        Страница редактирования поста не доступна авторизированному
        пользователю который не является автором
        """
        not_author = USER.objects.create_user(username='not-author')
        not_author_client = Client()
        not_author_client.force_login(not_author)
        response = not_author_client.get(reverse(
            'post_edit',
            kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            }
        ))
        self.assertNotEqual(response.status_code, 200)

    def test_post_url_exists_at_desired_loc(self):
        """
        Страница поста доступна любому пользователю
        """
        response = self.guest_client.get(reverse(
            'post',
            kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            }
        ))
        self.assertEqual(response.status_code, 200)

    def test_group_url_exists_at_desired_loc(self):
        """
        Страница сообщества доступна любому пользователю
        """
        response = self.guest_client.get(reverse(
            'group',
            kwargs={'slug': PostURLTests.group.slug}
        ))
        self.assertEqual(response.status_code, 200)

    def test_newpost_url_exists_at_desired_loc(self):
        """
        Страница new/ доступна авторизованному пользователю
        """
        response = self.authorised_client.get(reverse('new_post'))
        self.assertEqual(response.status_code, 200)

    def test_newpost_url_redirect_anonymous(self):
        """
        Страница new/ перенаправляет неавторизованного пользователя
        на страницу логина
        """
        response = self.guest_client.get(reverse('new_post'), follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')

    def test_edit_url_redirects_not_author(self):
        """
        Страница edit/ поста перенаправляет не автора
        на страницу поста
        """
        not_author = USER.objects.create_user(username='not-author')
        not_author_client = Client()
        not_author_client.force_login(not_author)
        response = not_author_client.get(reverse(
            'post_edit',
            kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            }),
            follow=True)
        self.assertRedirects(
            response, f'/{self.user.username}/{self.post.id}/')

    def test_edit_url_redirects_anonymous(self):
        """
        Страница edit/ поста перенаправляет неавторизованного
        пользователя на страницу авторизации
        """
        response = self.guest_client.get(reverse(
            'post_edit',
            kwargs={
                'username': self.user.username,
                'post_id': self.post.id
            }),
            follow=True)
        expected = (
            f'/auth/login/?next=/{self.user.username}/{self.post.id}/edit/'
        )
        self.assertRedirects(
            response, expected)

    def test_urls_uses_correct_template(self):
        """URL использует соответсвующий шаблон"""
        expected_pages = {
            reverse('new_post'): 'post_form.html',
            reverse('group', kwargs={'slug': 'test-slug'}): 'group.html',
            reverse('index'): 'index.html',
            reverse('post_edit',
                    kwargs={
                        'username': self.user.username,
                        'post_id': self.post.id}): 'post_form.html'
        }
        for url, template in expected_pages.items():
            with self.subTest(url=url):
                response = self.authorised_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_error_pages(self):
        """Сервер возвращает код если страница не найдена"""
        response = self.guest_client.get(reverse(
            'group',
            kwargs={'slug': 'doesnt-exist'}
        ))
        self.assertEqual(response.status_code, 404)
