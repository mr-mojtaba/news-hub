from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<pk>', views.PostDetailView, name='post_detail'),
]
