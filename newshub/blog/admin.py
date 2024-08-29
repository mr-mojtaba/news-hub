from django.contrib import admin

# Import models and necessary packages for customization of the admin panel.
from .models import *

# Need to install ( pip install django_jalali ) for using Jalali date filters.
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

# Customization of the Django admin site headers and titles
admin.sites.AdminSite.site_header = "پنل مدیریت جنگو"
admin.sites.AdminSite.site_title = "پنل"
admin.sites.AdminSite.index_title = "پنل مدیریت"


# Define inlines for related models to be displayed in the parent model’s admin page.
class ImageInline(admin.StackedInline):
    model = Image
    # No extra empty forms by default.
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    # No extra empty forms by default.
    extra = 0
    # Makes these fields read-only.
    readonly_fields = (
        'name',
        'body',
        'created',
    )


# Customize the Post model admin interface.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view of posts in the admin panel.
    list_display = [
        'title',
        'author',
        'publish',
        'status',
    ]

    # Default sorting order.
    ordering = [
        'title',
        'author',
    ]

    # Add a search bar with these fields as searchable.
    search_fields = [
        'title',
        'description',
    ]

    # Filters to allow admin to narrow down the list of posts.
    list_filter = [
        'status',
        'author',
        ('publish', JDateFieldListFilter),
    ]

    # Allow admins to pick authors from a list of IDs.
    raw_id_fields = [
        'author',
    ]

    # Enables navigation by date hierarchy.
    date_hierarchy = 'publish'

    # Automatically populates the slug field based on the title.
    prepopulated_fields = {
        'slug': ['title'],
    }

    # Allows editing the status directly from the list view.
    list_editable = [
        'status',
    ]

    # These fields will be clickable to view the detail page.
    list_display_links = [
        'title',
        'author',
        'publish',
    ]

    # Adds inlines for related images and comments.
    inlines = [
        ImageInline,
        CommentInline,
    ]


# Customize the Ticket model admin interface.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view of tickets in the admin panel.
    list_display = [
        'name',
        'subject',
        'phone',
    ]

    # These fields will be clickable to view the detail page.
    list_display_links = [
        'name',
        'subject',
        'phone',
    ]


# Customize the Comment model admin interface.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view of comments in the admin panel.
    list_display = [
        'post',
        'name',
        'created',
        'active',
    ]

    # Filters to allow admin to narrow down the list of comments.
    list_filter = [
        'active',
        ('created', JDateFieldListFilter),
        ('updated', JDateFieldListFilter),
    ]

    # Add a search bar with these fields as searchable.
    search_fields = [
        'name',
        'body',
    ]

    # Allows editing the active field directly from the list view.
    list_editable = [
        'active',
    ]


# Customize the Image model admin interface.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view of images in the admin panel.
    list_display = [
        'post',
        'title',
        'created',
    ]
