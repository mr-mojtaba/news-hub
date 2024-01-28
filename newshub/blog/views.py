from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView


# Create your views here.
def index(request):
    return HttpResponse('Index')


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    context = {
        'post': post,
    }
    return render(request, "blog/detail.html", context)


class PostListView(ListView):
    # Returns published posts.
    queryset = Post.published.all()

    # Defining name for the object.
    context_object_name = "posts"

    paginate_by = 3
    template_name = "blog/list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
