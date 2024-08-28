from django.db import models

# Standard python library imports.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Importing required modules from django_jalali
# (Install with: pip install django_jalali)
from django_jalali.db import models as jmodels
import jdatetime

# Importing ResizedImageField from django_resized
# (Install with: pip install django_resized)
from django_resized import ResizedImageField

from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


def get_upload_to(instance, filename):
    """
    Function to determine the file upload path for images.
    Uses the year of creation for organizing images into folders.
    """

    # Check if created has a value, otherwise use the current year.
    if instance.created:
        year = instance.created.year
    else:
        year = jdatetime.datetime.now().year
    return f'post_images/{year}/{filename}'


# Custom Managers
class PublishedManager(models.Manager):
    """
    Manager to handle queries for published posts.
    """
    def get_queryset(self):
        # Filter queryset to only include published posts.
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class DraftManager(models.Manager):
    """
    Manager to handle queries for draft posts.
    """
    def get_queryset(self):
        # Filter queryset to only include draft posts.
        return super().get_queryset().filter(status=Post.Status.DRAFT)


class RejectedManager(models.Manager):
    """
    Manager to handle queries for rejected posts.
    """
    def get_queryset(self):
        # Filter queryset to only include rejected posts.
        return super().get_queryset().filter(status=Post.Status.REJECTED)


# Model for Blog Post.
class Post(models.Model):
    """
    Model representing a blog post.
    """

    # Choices for the status of a post.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PU', 'Published'
        REJECTED = 'RJ', 'Rejected'

    # Fields for the Post model
    # Foreign key to the User model representing the author of the post.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_posts',
        verbose_name="نویسنده",
    )

    title = models.CharField(
        max_length=250,
        verbose_name="عنوان",
    )
    description = models.TextField(
        verbose_name="توضیحات",
    )

    slug = models.SlugField(
        max_length=250,
        verbose_name="نامک",
    )

    publish = jmodels.jDateTimeField(
        default=timezone.now,
        verbose_name="تاریخ انتشار",
    )

    created = jmodels.jDateTimeField(
        auto_now_add=True,
    )

    update = jmodels.jDateTimeField(
        auto_now=True,
    )

    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="وضعیت",
    )

    reading_time = models.PositiveIntegerField(
        verbose_name= "زمان مطالعه",
    )

    # Keeping the default manager(objects).
    objects = jmodels.jManager()

    # Managers for custom query sets.
    published = PublishedManager()
    draft = DraftManager()
    rejected = RejectedManager()

    class Meta:
        """
        Meta options for Post model.
        """

        # Default ordering by publish date in descending order.
        ordering = ['-publish']
        # Indexing for faster queries on publish date.
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    # String representation of the post.
    def __str__(self):
        """
        String representation of the Post model.
        """
        return self.title

    def get_absolute_url(self):
        """
        Method to get the URL for the post detail view.
        """
        return reverse('blog:post_detail', args=[self.id])


class Ticket(models.Model):
    """
    Model representing a ticket submitted by users.
    """

    message = models.TextField(
        verbose_name="پیام",
    )

    name = models.CharField(
        max_length=250,
        verbose_name="نام",
    )

    email = models.EmailField(
        verbose_name="ایمیل",
    )

    phone = models.CharField(
        max_length=11,
        verbose_name="شماره تماس",
    )

    subject = models.CharField(
        max_length=250,
        verbose_name="موضوع",
    )

    class Meta:
        """
        Meta options for Ticket model.
        """
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        """
        String representation of the Ticket model.
        """
        return self.subject


class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name="comments",
    )

    name = models.CharField(
        max_length=250,
        verbose_name="نام",
    )

    body = models.TextField(
        verbose_name="متن کامنت",
    )

    created = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated = jmodels.jDateTimeField(
        auto_now=True,
        verbose_name="تاریخ ویرایش",
    )

    active = models.BooleanField(
        default=False,
        verbose_name="وضعیت",
    )

    class Meta:
        """
        Meta options for Comment model.
        """

        # Default ordering by creation date in ascending order.
        ordering = ['created']
        # Indexing for faster queries on creation date.
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        """
        String representation of the Comment model.
        """
        return f"{self.name}: {self.post}"


class Image(models.Model):
    """
    Model representing an image associated with a blog post.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='پست',
    )

    image_file = ResizedImageField(
        upload_to=get_upload_to,
        size=[500, 500],
        quality=75,
        crop=['middle', 'center'],
        verbose_name='تصویر',
    )

    title = models.CharField(
        max_length=250,
        verbose_name='عنوان',
        null=True,
        blank=True,
    )

    description = models.TextField(
        verbose_name='توضیحات',
        null=True,
        blank=True,
    )

    created = jmodels.jDateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """
        Meta options for Image model.
        """

        # Default ordering by creation date in ascending order.
        ordering = [
            'created',
        ]
        # Indexing for faster queries on creation date.
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        """
        String representation of the Image model.
        """
        return self.title if self.title else self.image_file.name


# Signal to delete the image file after the object is deleted
@receiver(post_delete, sender=Image)
def delete_image_file_on_delete(sender, instance, **kwargs):
    """
    Signal receiver to delete the image file from the filesystem when an Image instance is deleted.
    """
    if instance.image_file:
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)
