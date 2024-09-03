from django.urls import path
from .views import (PostsList, PostDetail, PostByCategory, PostCreate, PostUpdate, PostDelete, after_logout,
                    OwnerCommentsView, OwnerPostsView, subscribe_to_newsletter)

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),    # post_list in this case is the name of the url pattern
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('category/<str:category_name>/', PostByCategory.as_view(), name='posts_by_category'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('logged_out', after_logout, name='after_logout'),
    path('my_comments/', OwnerCommentsView.as_view(), name='owner_comments'),
    path('my_posts/', OwnerPostsView.as_view(), name='owner_posts'),
    path('subscribe/', subscribe_to_newsletter, name='subscribe_to_newsletter')
]
