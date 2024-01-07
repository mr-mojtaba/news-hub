from django.db import models

# Standard python library
from django.utils import timezone
from django.contrib.auth.models import User


# Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.DRAFT)


class RejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.REJECTED)


# Create your models here.
class Post(models.Model):
    # Creating a class for posts status.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PU', 'Published'
        REJECTED = 'RJ', 'Rejected'

    # Creating a many-to-one field for user.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_posts'
    )

    # To create fields.
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)

    # Date of publication.
    publish = models.DateTimeField(default=timezone.now)

    # Recording the moment the post was created.
    created = models.DateTimeField(auto_now_add=True)

    # Date of update.
    update = models.DateTimeField(auto_now=True)

    # Creating a field for Status class.
    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # Keeping the default manager(objects).
    objects = models.Manager()
    # Create object from PublishedManager.
    published = PublishedManager()
    draft = DraftManager()
    rejected = RejectedManager()

    class Meta:
        # Sorting the table by publish.
        ordering = ['-publish']
        # Specifying the indexing.
        indexes = [
            models.Index(fields=['-publish'])
        ]

    # Overwriting the method as the title.
    def __str__(self):
        return self.title
