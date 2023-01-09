from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.cache import cache_page


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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


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
        today = datetime.now(timezone.utc)
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        count = Post.objects.filter(create_date__gte=today).filter(user=post.user).count()
        if count >= 3:
            return redirect('/news/error')
            # return render(request, 'error.html', status=404)
        else:
            post.save()
            post.category.add(request.POST['category'])
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


@login_required
def subscribe(request):
    user = request.user
    category = Category.objects.get(category=request.POST.get('subscribe'))
    category.subscribers.add(user)
    return redirect('/news/')


def error(request):
    return render(request, 'error.html')
