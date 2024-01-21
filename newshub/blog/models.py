from django.db import models

# Standard python library
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Need to install ( pip install django_jalali )
from django_jalali.db import models as jmodels


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
        related_name='user_posts',
        verbose_name="نویسنده"
    )

    # To create fields.
    title = models.CharField(
        max_length=250,
        verbose_name="عنوان"
    )
    description = models.TextField(
        verbose_name="توضیحات"
    )

    slug = models.SlugField(
        max_length=250,
        verbose_name="نامک"
    )

    # Date of publication.
    publish = jmodels.jDateTimeField(
        default=timezone.now,
        verbose_name="تاریخ انتشار"
    )

    # Recording the moment the post was created.
    created = jmodels.jDateTimeField(
        auto_now_add=True
    )

    # Date of update.
    update = jmodels.jDateTimeField(
        auto_now=True
    )

    # Creating a field for Status class.
    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="وضعیت"
    )

    # Keeping the default manager(objects).
    objects = jmodels.jManager()

    # Create customize managers.
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
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    # Overwriting the method as the title.
    def __str__(self):
        return self.title

    # For creating URL.
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])
