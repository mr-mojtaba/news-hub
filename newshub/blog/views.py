from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


# Create your views here.
def index(request):
    return HttpResponse('Index')


def post_list(request):
    posts = Post.published.all()

    # # Creating an object of the paginator class.
    paginator = Paginator(posts, 3)
    # Specifying the page number.
    page_number = request.GET.get('page', 1)
    # Resetting the value with page_number.
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {
        'posts': posts,
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    context = {
        'post': post,
    }
    return render(request, "blog/detail.html", context)


class PostListView(ListView):
    paginate_by = 3
    template_name = "blog/list.html"
    queryset = Post.published.all()
    context_object_name = "posts"
