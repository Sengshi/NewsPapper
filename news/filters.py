from django import forms
from django_filters import FilterSet, DateTimeFilter, CharFilter
from .models import Post


class PostFilter(FilterSet):
    date = DateTimeFilter(field_name="create_date", lookup_expr='gt', label="Дата создания от",
                          widget=forms.DateInput(attrs={'type': 'date'}))
    title = CharFilter(field_name="title", lookup_expr='icontains', label="Название содержит")

    class Meta:
        model = Post
        fields = ('date', 'title', 'user', 'category')
