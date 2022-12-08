from itertools import count

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-create_date')
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-create_date')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostAdd(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'post_add.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        post = Post(
            user=Author.objects.get(user=request.POST['user']),
            view=request.POST['view'],
            title=request.POST['title'],
            post=request.POST['post'],
        )
        post.save()
        post.category.set(request.POST['category'])

        send_mail(
            subject=f'{post.title}',
            message=post.post,
            from_email='testpysend@mail.ru',
            recipient_list=['asket2013@yandex.ru', ]
        )
        return redirect('/news/')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
