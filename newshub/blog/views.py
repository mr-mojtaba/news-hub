from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST


# Create your views here.
def index(request):
    return HttpResponse('Index')


class PostListView(ListView):
    # Returns published posts.
    queryset = Post.published.all()

    # Defining name for the object.
    context_object_name = "posts"

    paginate_by = 3
    template_name = "blog/list.html"


def post_detail(request, id):
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED
    )

    # Creating a variable and put the approved comments in it.
    comments = post.comments.filter(active=True)

    # Creating an empty form.
    form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }

    return render(
        request,
        "blog/detail.html",
        context
    )


def ticket(request):
    if request.method == "POST":
        # Creating a Variable from the TicketForm.
        form = TicketForm(request.POST)

        # Form data validation.
        if form.is_valid():
            # Creating a variable and assigning it with form values.
            # (cleaned_data is a dictionary).
            cd = form.cleaned_data

            # Creating a tuple from the Ticket model.
            Ticket.objects.create(
                #  Initialization of each Ticket field with the values of each Ticket Form field.
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject'],
            )
            return redirect('blog:ticket')
    else:
        # Creating a variable from TicketForm with no value.
        form = TicketForm()

    # Show ticket.html page.
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(
        request,
        "forms/comment.html",
        context,
    )
