from django.contrib import admin

# For customization of the admin panel
from .models import *

# Need to install ( pip install django_jalali )
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

admin.sites.AdminSite.site_header = "پنل مدیریت جنگو"
admin.sites.AdminSite.site_title = "پنل"
admin.sites.AdminSite.index_title = "پنل مدیریت"


# Register your models here.
# Customization of the admin panel.

#Inlines
class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = (
        'name',
        'body',
        'created',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Showing these fields in the top bar of the posts display.
    list_display = ['title', 'author', 'publish', 'status']

    # Defining the default list for sorting fields.
    ordering = ['title', 'author']

    # Creating a search bar and a list of searchable fields.
    search_fields = ['title', 'description']

    # Creating a filter page and a list of filterable fields.
    list_filter = ['status', 'author', ('publish', JDateFieldListFilter)]

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

    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Showing these fields in the top bar of the posts display.
    list_display = [
        'post',
        'name',
        'created',
        'active',
    ]

    # Creating a filter page and a list of filterable fields.
    list_filter = [
        'active',
        ('created', JDateFieldListFilter),
        ('updated', JDateFieldListFilter),
    ]

    # Creating a search bar and a list of searchable fields.
    search_fields = [
        'name',
        'body',
    ]

    # Creating the ability to edit each field in the table.
    list_editable = [
        'active'
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [
        'post',
        'title',
    ]
