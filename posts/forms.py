from django.forms import ModelForm
from .models import Post, Group


class CreationForm(ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'group', 'description', 'website')
        labels = {'name': 'Желание',
                  'group': 'Праздник',
                  'description': 'Описание',
                  'website': 'Сайт'
                  }

    class Meta1:
        model = Group
        fields = ('title', 'slug', 'description')
        labels = {'title': 'Название',
                  'slug': 'Адрес',
                  'description': 'Описание'
                  }


