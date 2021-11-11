from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Group, User, Post


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='yes'
        )

        Group.objects.create(
            title='Крутое название',
            slug='cool_address',
            description='Крутое описание',
            author=cls.user
        )

        cls.post = Post.objects.create(
            text='Крутой текст',
            author=cls.user,

        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        # self.user = User.objects.create_user(username='test_username')
        self.user = TaskURLTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage_template(self):
        '''Тест работы стартовой страницы'''
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_template(self):
        '''Group page works'''
        response = self.guest_client.get('/group/cool_address/')
        self.assertEqual(response.status_code, 200)

    def test_new_unauthorized(self):
        '''New is unavailable for anonymous users'''
        response = self.guest_client.get('/new')
        self.assertEqual(response.status_code, 302)

    def test_new_authorized(self):
        '''New is available for authorized users'''
        response = self.authorized_client.get('/new')
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        '''templates work fine'''
        templates = {
            '/': 'index.html',
            '/new': 'new.html',
            '/group/cool_address/': 'group.html',
            f'/{TaskURLTests.user}/{TaskURLTests.post.id}': 'post.html',

        }
        for value, expected in templates.items():
            with self.subTest(value=value):
                self.assertTemplateUsed(
                    self.authorized_client.get(value), expected)

    def test_profile(self):
        '''Profile is acceptable'''
        response = self.authorized_client.get(f'/{TaskURLTests.user}/')
        self.assertEqual(response.status_code, 200)

    def test_post_available_for_authorized(self):
        '''Post is available for authorized'''
        response = self.authorized_client.get(f'/{TaskURLTests.user}/{TaskURLTests.post.id}')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_available_for_author(self):
        '''Post edit is available for authorized'''
        response = self.authorized_client.get(f'/{TaskURLTests.user}/{TaskURLTests.post.id}/edit')
        self.assertEqual(response.status_code, 200)

    def test_post_not_available_for_unauthorized(self):
        '''Post edit is not available for unauthorized'''
        response = self.guest_client.get(f'/{TaskURLTests.user}/{TaskURLTests.post.id}/edit')
        self.assertEqual(response.status_code, 302)

    def test_post_not_available_for_not_author(self):
        '''Post edit is not available for not author'''
        self.user_1 = User.objects.create(
            username='test_user'
        )
        self.wrong_author = Client()
        self.wrong_author.force_login(self.user_1)

        response = self.wrong_author.get(
            f'/{TaskURLTests.user.username}/{TaskURLTests.post.id}/edit', follow=True)
        self.assertRedirects(response, reverse('index'))

