from django import template
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Max, Min
from ..models import Post, Comment

# Need to install ( pip install markdown )
from markdown import markdown

# To build trust for markdown
from django.utils.safestring import mark_safe

# Creating an object to access the simple_tag decorator
register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag
def last_post_date():
    return Post.published.first().publish.strftime('%H:%M - %Y/%m/%d')


@register.simple_tag
def most_popular_posts(count=5):
    return Post.published.annotate(
        comments_count=Count('comments')
    ).order_by('-comments_count')[:count]


@register.simple_tag
def most_reading_time_post():
    post = Post.published.order_by('-reading_time').first()
    if post:
        return {
            'name': post.title,
            'link': post.get_absolute_url,
        }
    return None


@register.simple_tag
def most_reading_time():
    mrt = Post.published.aggregate(Max('reading_time'))
    return mrt['reading_time__max']


@register.simple_tag
def least_reading_time_post():
    post = Post.published.order_by('reading_time').first()
    if post:
        return {
            'name': post.title,
            'link': post.get_absolute_url(),
        }
    return None


@register.simple_tag
def least_reading_time():
    lrt = Post.published.aggregate(Min('reading_time'))
    return lrt['reading_time__min']


@register.simple_tag
def most_active_users(count=2):
    users = User.objects.annotate(
        num_posts=models.Count('user_posts'),
    ).order_by('-num_posts')[:count]
    return users


@register.inclusion_tag("partials/latest_posts.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts,
    }
    return context


@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))


@register.filter
def censor_text(value):
    censored_words = [
        'فحش',
        'خراب',
        'بدکاره',
    ]
    for word in censored_words:
        value = value.replace(word, "'سانسور'")
    return value
