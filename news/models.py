from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        sum_post_rating = 0
        post_rating = self.post_set.all().aggregate(postRating=Sum("rating"))
        sum_post_rating += post_rating.get("postRating")
        sum_comment_rating = 0
        comment_rating = self.user.comment_set.all().aggregate(commentRating=Sum("rating"))
        sum_comment_rating += comment_rating.get("commentRating")
        self.rating = sum_post_rating * 3 + sum_comment_rating
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return self.category


class Post(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)

    news = 'nw'
    article = 'ar'
    POSITIONS = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]

    view = models.CharField(max_length=2, choices=POSITIONS, default=article)
    title = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    post = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title

    def preview(self):
        return f'{self.post[0:123]}...'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
