from django.db import models

# Standard python library
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Need to install ( pip install django_jalali )
from django_jalali.db import models as jmodels

# Need to install ( pip install django_resized )
from django_resized import ResizedImageField

from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


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
        verbose_name="نویسنده",
    )

    # To create fields.
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

    # Date of publication.
    publish = jmodels.jDateTimeField(
        default=timezone.now,
        verbose_name="تاریخ انتشار",
    )

    # Recording the moment the post was created.
    created = jmodels.jDateTimeField(
        auto_now_add=True,
    )

    # Date of update.
    update = jmodels.jDateTimeField(
        auto_now=True,
    )

    # Creating a field for Status class.
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


class Ticket(models.Model):
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
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.subject


class Comment(models.Model):
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
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name}: {self.post}"


class Image(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='پست',
    )

    image_file = ResizedImageField(
        upload_to='post_image/',
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
        ordering = [
            'created',
        ]
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        return self.title if self.title else self.image_file.name


# Signal to delete the image file after the object is deleted
@receiver(post_delete, sender=Image)
def delete_image_file_on_delete(sender, instance, **kwargs):
    if instance.image_file:
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)
