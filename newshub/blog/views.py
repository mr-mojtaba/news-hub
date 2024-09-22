from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity


# View to render the index page.
def index(request):
    return render(
        request,
        "blog/index.html",
    )


class PostListView(ListView):
    # Returns all published posts.
    queryset = Post.published.all()

    # Defines the context variable name for the list of posts.
    context_object_name = "posts"

    # Sets the number of posts per page for pagination
    paginate_by = 3
    template_name = "blog/list.html"


def post_detail(request, id):
    # Retrieve the post by id, raising a 404 error if not found or not published.
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED,
    )

    # Filter and retrieve active comments related to the post.
    comments = post.comments.filter(active=True)

    # Initialize an empty comment form.
    form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }

    # Render the post detail page with the post, comments, and form.
    return render(
        request,
        "blog/detail.html",
        context,
    )


def ticket(request):
    if request.method == "POST":
        # Initialize the form with POST data.
        form = TicketForm(request.POST)

        # Validate the form data.
        if form.is_valid():
            # Cleaned data is a dictionary containing form values.
            cd = form.cleaned_data

            # Create a new Ticket object using the cleaned data.
            Ticket.objects.create(
                #  Initialization of each Ticket field with the values of each Ticket Form field.
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject'],
            )

            # Redirect to the ticket page after saving.
            return redirect('blog:ticket')
    else:
        # Initialize an empty form.
        form = TicketForm()

    # Render the ticket form page.
    return render(
        request,
        'forms/ticket.html',
        {'form': form},
    )


@require_POST
def post_comment(request, post_id):
    # Retrieve the post by id, raising a 404 error if not found or not published.
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )

    comment = None

    # Initialize the comment form with POST data.
    form = CommentForm(data=request.POST)

    # If the form is valid, save the comment without committing.
    if form.is_valid():
        # Save the comment without committing.
        comment = form.save(commit=False)
        # Associate the comment with the post.
        comment.post = post
        # Save the comment to the database.
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }

    # Render the comment form and related post information.
    return render(
        request,
        "forms/comment.html",
        context,
    )


@login_required(login_url='/admin/login/')
def create_post(request):
    if request.method == 'POST':
        # Initialize the form with POST data.
        form = CreatePostForm(request.POST, request.FILES)

        # Validate the form data.
        if form.is_valid():
            # Save the post without committing.
            post = form.save(commit=False)
            # Assign the current user as the author of the post.
            post.author = request.user
            # Save the post to the database.
            post.save()

            Image.objects.create(
                image_file=form.cleaned_data['image1'],
                post=post,
            )
            Image.objects.create(
                image_file=form.cleaned_data['image2'],
                post=post,
            )

            return redirect('blog:profile')
    else:
        # Initialize an empty form.
        form = CreatePostForm()

    # Render the post creation form page.
    return render(
        request,
        'forms/create-post.html',
        {'form': form},
    )


def post_search(request):
    query = None
    results = []

    if 'query' in request.GET:
        # Initialize the search form with GET data.
        form = SearchForm(
            data=request.GET,
        )

        if form.is_valid():
            # Get the cleaned search query.
            query = form.cleaned_data['query']

            # Search for posts with similar titles
            results1 = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(
                similarity__gt=0.1,
            ).order_by(
                '-similarity',
            )

            # Search for posts with similar descriptions.
            results2 = Post.published.annotate(
                similarity=TrigramSimilarity('description', query),
            ).filter(
                similarity__gt=0.1,
            ).order_by(
                '-similarity',
            )

            # Search for images with similar titles.
            image_results1 = Image.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(
                similarity__gt=0.1,
            ).order_by(
                '-similarity',
            )

            # Search for images with similar descriptions.
            image_results2 = Image.objects.annotate(
                similarity=TrigramSimilarity('description', query),
            ).filter(
                similarity__gt=0.1,
            ).order_by(
                '-similarity',
            )

            # Get the related posts for images matching the search query.
            post_results_from_image1 = [img.post for img in image_results1]
            post_results_from_image2 = [img.post for img in image_results2]

            # Combine all search results into one list.
            combined_results = (
                    list(results1)
                    + list(results2)
                    + post_results_from_image1
                    + post_results_from_image2
            )

            # Sort and remove duplicates from the combined results based on similarity.
            results = sorted(
                set(combined_results),
                key=lambda x: x.similarity if hasattr(x, 'similarity') else 0,
                reverse=True,
            )

        context = {
            'query': query,
            'results': results,
        }

        # Render the search results page.
        return render(
            request,
            'blog/search.html',
            context,
        )


@login_required(login_url='/admin/login/')
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)

    context = {
        'posts': posts,
    }

    return render(
        request,
        'blog/profile.html',
        context,
    )


@login_required(login_url='/admin/login/')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')

    return render(
        request,
        'forms/delete-post.html',
        {'post': post},
    )
