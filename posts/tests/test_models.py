from django.test import TestCase

from posts.models import Group, Post, User


class GroupModelTest(TestCase):
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

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_verboses = {
            'title': 'Название',
            'description': 'Описание'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_help_texts = {
            'title': 'Введите Название',
            'description': 'Введите Описание'

        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_str(self):
        line = 'Крутое название'
        self.assertEqual(GroupModelTest.group.__str__(), line)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(
            username='Чел'
        )

        cls.post = Post.objects.create(
            text='Крутой текст',
            author=cls.user

        )

    def test_verbose_name_post(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст',

        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_help_text_post(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст',

        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_str_post(self):
        line = 'Крутой текст'
        self.assertEqual(PostModelTest.post.__str__(), line)
