from django.contrib import admin
from .models import Post, Category, Comment, Reply


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'comments_count', 'content', 'author']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'date_commented')


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)
