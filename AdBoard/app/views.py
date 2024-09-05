from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Subscription
from django.shortcuts import get_object_or_404, redirect
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CommentForm
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


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
                try:
                    comment.save()
                    messages.success(self.request, 'Your comment has been successfully submitted for approval!')
                    return redirect('post_detail', pk=post.pk)

                except Exception as e:
                    print(e)
                    messages.warning(self.request, 'Comment submitted but a notification could not be sent.')
                return redirect('post_detail', pk=post.pk)

            else:
                return redirect('login')  # Redirect to login if user is not authenticated

        else:
            messages.error(self.request, 'There was an error with your comment. Please try again.')


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
    success_url = reverse_lazy('post_list')

    #   Override the form_valid method in order to display messages after post creation
    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            response = super().form_valid(form)
            messages.success(self.request, 'Your post has been successfully created!')
            return response

        except Exception as e:
            print(e)
            messages.error(self.request, f'An error occurred while trying create post. Try again later')
            return self.form_invalid(form)  # Handle the form as invalid if an error occurs


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('app.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'update_post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Your post has been successfully updated!')
            return response
        except Exception as e:
            messages.error(self.request, f'An error occurred while trying update post. Try again later')
            return self.form_invalid(form)  # Handle the form as invalid if an error occurs


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('app.delete_post',)
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('post_list')

    #   Override the delete method to display messages of successful deletion
    def form_valid(self, form):
        try:
            logger.debug("Delete method called")
            response = super().form_valid(form)
            messages.success(self.request, 'Your post has been successfully deleted!')
            return response
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            messages.error(self.request, 'An error occurred while trying to delete the post. Please try again later.')
            return self.form_invalid(form)  # Redirect to the post list even if deletion fails

    def form_invalid(self, form):
        """
        Handle the case when form is invalid.
        """
        return super().form_invalid(form)


def after_logout(request):
    return render(request, 'logout_confirmation.html')


class OwnerCommentsView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'owner_comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post__author=self.request.user,
                                      is_approved=False)  # Unapproved comments by post owner

    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        action = request.POST.get('action')
        comment = get_object_or_404(Comment, id=comment_id, post__author=request.user)

        if action == 'approve':
            comment.is_approved = True
            comment.save()
            messages.success(request, f'You have successfully approved {comment.author} comment!')
        elif action == 'delete':
            try:
                comment.delete()
                messages.info(request, f'You have successfully deleted {comment.author} comment')
            except Exception as e:
                messages.error(request, f'An error occurred while trying to delete the comment. Try again later')

        return redirect('owner_comments')  # Redirect to the same page after action


class OwnerPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'owner_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Get all posts created by the logged-in user
        user_posts = Post.objects.filter(author=self.request.user)
        # Get all comments related to those posts
        return user_posts


@login_required
def subscribe_to_newsletter(request):
    subscription, created = Subscription.objects.get_or_create(user=request.user)
    if created:
        messages.success(request, f'You have successfully subscribed to newsletter!')
    else:
        messages.info(request, 'You are already subscribed to the newsletter.')
    return redirect('post_list')    # Redirect to the main page
