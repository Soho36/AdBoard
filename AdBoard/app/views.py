from django.views.generic import ListView, DetailView
from .models import Post, Category
from django.shortcuts import get_object_or_404


class PostsList(ListView):
    model = Post
    ordering = 'name'
    template_name = 'post_list.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'


class PostByCategory(ListView):
    template_name = 'post_by_category.html'
    context_object_name = 'post_by_category'

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        self.category = get_object_or_404(Category, name__iexact=category_name)
        return Post.objects.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the category object to the context
        context['category'] = self.category
        return context
