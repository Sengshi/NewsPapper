from django.contrib.auth.models import User
from django.db import models


news = 'news'
article = 'article'
POSITIONS = [
    (news, 'Новость'),
    (article, 'Статья'),
]


class Author(models.Model):
    rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    view = models.CharField(max_length=10, choices=POSITIONS)
    title = models.CharField(max_length=255)
    rating = models.FloatField(default=0.0)
    post = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)
