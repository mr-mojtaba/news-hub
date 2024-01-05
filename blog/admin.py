from django.contrib import admin

# For customization of the admin panel
from .models import *


# Register your models here.
# Customization of the admin panel.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Showing these fields in the top bar of the posts display.
    list_display = ['title', 'author', 'publish', 'status']

    # Defining the default list for sorting fields.
    ordering = ['title', 'author']

    # Creating a search bar and a list of searchable fields.
    search_fields = ['title', 'description']

    # Creating a filter page and a list of filterable fields.
    list_filter = ['status', 'author', 'publish']

    # Assigning an ID to each author and
    # changing the type of author editing in the post manager.
    raw_id_fields = ['author']

    # Creating a time hierarchy filter based on a field.
    date_hierarchy = 'publish'

    # To automatically complete the slug field based on title.
    prepopulated_fields = {'slug': ['title']}

    # Creating the ability to edit each field in the table.
    list_editable = ['status']

    # Converting each field to a link for opening the post manager page.
    list_display_links = ['title', 'author', 'publish']
