from django.test import Client, TestCase
from posts.models import Post
from posts.forms import PostForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
import shutil
import tempfile

USER = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.guest_client = Client()
        cls.test_user = USER.objects.create_user(username='tester')
        cls.authorised_client = Client()
        cls.authorised_client.force_login(cls.test_user)
        cls.post = Post.objects.create(
            text='Тестовый текст поста',
            author=cls.test_user,
        )
        cls.form = PostForm()
        cls.image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_text_label(self):
        """label поля text соответствует заданному"""
        title_label = PostFormTest.form.fields['text'].label
        self.assertEqual(title_label, 'Текст поста')

    def test_newpost_created(self):
        """При отправке формы создается новый пост в БД"""
        user_client = PostFormTest.authorised_client
        form_data = {
            'text': 'Тестовый пост',
            'author': PostFormTest.test_user,
            'image': PostFormTest.image
        }
        post_count = Post.objects.count()
        user_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count + 1)

    def test_editpost_edites_db_object(self):
        """При отправке формы соответствующий объект изменяется в БД"""
        user_client = PostFormTest.authorised_client
        form_data = {
            'text': 'Измененный текст поста',
            'author': PostFormTest.test_user
        }
        user_client.post(
            reverse('post_edit', kwargs={
                'username': PostFormTest.test_user.username,
                'post_id': PostFormTest.post.id
            }),
            data=form_data,
            follow=True
        )
        response = Post.objects.get(pk=1).text
        self.assertEqual(response, form_data['text'])

    def test_editpost_db_object_for_anonymous(self):
        """
        При отправке формы объект не изменяется в БД
        """
        user_client = PostFormTest.guest_client
        form_data = {
            'text': 'Измененный текст поста',
        }
        user_client.post(
            reverse('post_edit', kwargs={
                'username': PostFormTest.test_user.username,
                'post_id': PostFormTest.post.id
            }),
            data=form_data,
            follow=True
        )
        response = Post.objects.get(pk=1).text
        not_changed_text = PostFormTest.post.text
        self.assertEqual(response, not_changed_text)

    def test_editpost_db_object_for_not_author(self):
        """
        При отправке формы не автором  объект не изменяется в БД
        """
        not_author = USER.objects.create_user(username='not-author')
        not_author_client = Client()
        not_author_client.force_login(not_author)
        form_data = {
            'text': 'Измененный текст поста',
            'author': PostFormTest.test_user
        }
        not_author_client.post(
            reverse('post_edit', kwargs={
                'username': PostFormTest.test_user.username,
                'post_id': PostFormTest.post.id
            }),
            data=form_data,
            follow=True
        )
        response = Post.objects.get(pk=1).text
        not_changed_text = PostFormTest.post.text
        self.assertEqual(response, not_changed_text)
