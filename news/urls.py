from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostAdd, PostDelete, PostEdit, subscribe, error

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('add/', PostAdd.as_view(), name='post_add'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit', PostEdit.as_view(), name='post_update'),
    path('search', PostSearch.as_view()),
    path('error', error, name='error'),
    path('subscribe', subscribe, name='subscribe'),
]
