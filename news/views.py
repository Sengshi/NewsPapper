from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Author, Category, UserCategory
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
        for _ in UserCategory.objects.filter(category=request.POST['category']).values("user"):
            subscriber = User.objects.get(id=_["user"])
            recipient = [subscriber.email]

            html_content = render_to_string(
                'news_created.html',
                {
                    'post': post,
                    'subscriber': subscriber,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{post.title}',
                body=post.post,
                from_email='testpysend@mail.ru',
                to=recipient,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

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
