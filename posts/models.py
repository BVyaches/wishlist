from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
	title = models.CharField(max_length=15, help_text='Введите Название Праздника',
	                         verbose_name='Название', )
	slug = models.SlugField(unique=True)
	description = models.TextField(help_text='Введите дату',
	                               verbose_name='Дата', )
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title


class Post(models.Model):
	name = models.TextField(help_text='Ваше желание', verbose_name='Желание')
	description = models.TextField(help_text='Введите описание желания',
	                               verbose_name='Описание', blank=False,
	                               null=False)
	website = models.URLField(help_text='Скопируйте ссылку на желание',
	                          verbose_name='Ссылка', blank=True, null=True)
	pub_date = models.DateTimeField('date published', auto_now_add=True)

	author = models.ForeignKey(User, on_delete=models.CASCADE,
	                           related_name='posts', )

	group = models.ForeignKey(
		Group,
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)

	def __str__(self):
		return self.name[:15]

	class Meta:
		ordering = ('-pub_date',)
