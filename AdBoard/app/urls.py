from django.urls import path
from .views import PostsList, PostDetail, PostByCategory

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<str:category_name>/', PostByCategory.as_view(), name='posts_by_category'),
]
