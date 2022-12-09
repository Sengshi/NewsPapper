from django import forms
from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    date = DateTimeFilter(field_name="create_date", lookup_expr='gt', label="Дата создания от",
                          widget=forms.DateInput(attrs={'type': 'date'}))
    title = CharFilter(field_name="title", lookup_expr='icontains', label="Название содержит")
    category = ModelChoiceFilter(label="Категория", queryset=Category.objects.all(), to_field_name="category")

    class Meta:
        model = Post
        fields = ('date', 'title', 'user', 'category')
