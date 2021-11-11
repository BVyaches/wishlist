from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post

User = get_user_model()


class GroupPostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='yes'
        )

        cls.group = Group.objects.create(
            title='Крутое название',
            slug='cool_address',
            description='Крутое описание',
            author=cls.user
        )
        cls.post = Post.objects.create(
            text='Крутой текст',
            author=cls.user,
            group=cls.group

        )

    def setUp(self):
        # Создаём неавторизованный клиент
        self.guest_client = Client()
        # Создаём авторизованный клиент
        self.user = GroupPostPagesTest.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_page_names = {
            'group.html': reverse('group_posts', kwargs={'slug':
                                                             'cool_address'}),
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),

        }
        # Проверяем, что при обращении к name
        # вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_new_post_show_correct_context(self):
        """Шаблон new сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {

            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField

        }

        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_home_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым

        first_object = response.context['page'][0]
        task_text_0 = first_object.text
        task_author_0 = first_object.author.username
        task_group_0 = first_object.group.title
        self.assertEqual(task_author_0, 'yes')
        self.assertEqual(task_text_0, 'Крутой текст')
        self.assertEqual(task_group_0, 'Крутое название')

    def test_group_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'cool_address'}))
        self.assertEqual(response.context['group'].title, 'Крутое название')
        self.assertEqual(response.context['group'].description,
                         'Крутое описание')
        self.assertEqual(response.context['group'].slug, 'cool_address')

    def test_initial_value(self):
        '''Post creates'''
        posts_count = Post.objects.count()

        Post.objects.create(
            text='Крутой текст1',
            author=GroupPostPagesTest.user,
            group=GroupPostPagesTest.group

        )

        self.assertEqual(posts_count + 1, Post.objects.count())

    def test_post_edit_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        # response = self.authorized_client.get(
        #   reverse('post_edit', kwargs={'username': 'yes', 'post_id': GroupPostPagesTest.post.id}))
        response = self.authorized_client.get(f'/{GroupPostPagesTest.user}/{GroupPostPagesTest.post.id}', )

        self.assertEqual(response.context['post'].text, 'Крутой текст')
        self.assertEqual(response.context['post'].group.title,
                         'Крутое название')

    def test_post_view_context(self):
        """Шаблон post_view сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('post', kwargs={'username':
                                        GroupPostPagesTest.user.username,
                                    'post_id':
                                        GroupPostPagesTest.post.id}))
        self.assertEqual(response.context['post'].text, 'Крутой текст')
        self.assertEqual(response.context['user'].username, 'yes')
        self.assertEqual(response.context['post'].group.title,
                         'Крутое название')

    def test_profile_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('profile', kwargs={'username':
                                           GroupPostPagesTest.user.username,
                                       }))
        self.assertEqual(response.context['user'].username, 'yes')


class PaginatorViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='Чел'
        )

        cls.group = Group.objects.create(
            title='Крутое название',
            slug='cool_address',
            description='Крутое описание',
            author=cls.user
        )
        for i in range(15):
            Post.objects.create(
                text='Крутой текст',
                author=cls.user,
                group=cls.group)

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_five_records(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 5)
