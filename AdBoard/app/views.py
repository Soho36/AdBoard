from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from django.shortcuts import get_object_or_404, redirect
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from .forms import CommentForm


class PostsList(ListView):
    model = Post
    ordering = '-published_date'
    template_name = 'post_list.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            post = self.get_object()
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            return redirect('login')  # Redirect to login if user is not authenticated


class PostByCategory(ListView, LoginRequiredMixin, PermissionRequiredMixin):
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


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('app.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'add_post_form.html'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('app.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'update_post_form.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('app.delete_post',)
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('post_list')


def after_logout(request):
    return render(request, 'logout_confirmation.html')


class OwnerCommentsView(LoginRequiredMixin, ListView):
    # model = Comment
    # template_name = 'owner_comments.html'
    # context_object_name = 'comments'
    #
    # def get_queryset(self):
    #     # Get all posts created by the logged-in user
    #     user_posts = Post.objects.filter(author=self.request.user)
    #     # Get all comments related to those posts
    #     return Comment.objects.filter(post__in=user_posts).order_by('-created_at')
    model = Comment
    template_name = 'owner_comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post__author=self.request.user,
                                      is_approved=False)  # Unapproved comments by post owner

    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, post__author=request.user)
        comment.is_approved = True
        comment.save()
        return redirect('owner_comments')  # Redirect to the same page after approval


class OwnerPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'owner_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Get all posts created by the logged-in user
        user_posts = Post.objects.filter(author=self.request.user)
        # Get all comments related to those posts
        return user_posts

