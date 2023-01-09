from django.contrib import admin

from .models import Category, Author, Post, PostCategory, Comment, UserCategory


class UserCategoryAdm(admin.ModelAdmin):
    list_display = ('category', 'user')
    list_filter = ('category', )
    search_fields = ('user',)


class AuthorAdm(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('rating',)
    search_fields = ('user',)


class PostAdm(admin.ModelAdmin):
    list_display = ('user', 'title', 'rating', )
    list_filter = ('rating', 'user',)
    search_fields = ('user', 'title',)


class PostCategoryAdm(admin.ModelAdmin):
    list_display = ('category', 'post')
    list_filter = ('category', )
    search_fields = ('post',)


class CommentAdm(admin.ModelAdmin):
    list_display = ('user', 'post', 'rating',)
    list_filter = ('post', 'user', 'rating',)
    search_fields = ('post',)


class CategoryAdm(admin.ModelAdmin):
    list_display = ('category',)
    list_filter = ('category',)


admin.site.register(UserCategory, UserCategoryAdm)
admin.site.register(Author, AuthorAdm)
admin.site.register(Post, PostAdm)
admin.site.register(PostCategory, PostCategoryAdm)
admin.site.register(Comment, CommentAdm)
admin.site.register(Category, CategoryAdm)
