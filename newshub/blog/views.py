from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView


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


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"


def ticket(request):
    if request.method == "POST":
        # Creating a Variable from the TicketForm.
        form = TicketForm(request.POST)

        # Form data validation.
        if form.is_valid():
            # Creating an object from the Ticket model.
            ticket_obj = Ticket.objects.create()

            # Creating a variable and assigning it with form values.
            # (cleaned_data is a dictionary).
            cd = form.cleaned_data

            #  Initialization of each Ticket field with the values of each Ticket Form field.
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']

            # Storage in the database.
            ticket_obj.save()

            return redirect('blog:ticket')
    else:
        # Creating a variable from TicketForm with no value.
        form = TicketForm()

    # Show ticket.html page.
    return render(request, 'forms/ticket.html', {'form': form})
