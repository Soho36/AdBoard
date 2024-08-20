from django.urls import path
from .views import PostsList, PostDetail, PostByCategory, PostCreate

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),    # post_list in this case is the name of the url pattern
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('category/<str:category_name>/', PostByCategory.as_view(), name='posts_by_category'),
    path('create/', PostCreate.as_view(), name='post_create'),
]
