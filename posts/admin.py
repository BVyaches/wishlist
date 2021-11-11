from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'pub_date', 'author')
    search_fields = ('name',)
    list_filter = ('pub_date',)
    empty_value_display = '-pusto-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
