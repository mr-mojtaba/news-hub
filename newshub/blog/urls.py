from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:id>', views.post_detail, name='post_detail'),
    path('ticket', views.ticket, name='ticket'),
    path('posts/<int:post_id>/comment', views.post_comment, name='post_comment'),
    path('search/', views.post_search, name='post_search'),
    path('profile/', views.profile, name='profile'),
    path('profile/create_post/', views.create_post, name='create_post'),
    path('profile/delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]
