from django import template
from ..models import Post, Comment

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


@register.inclusion_tag("partials/latest_posts.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts,
    }
    return context
