from django import template
from ..models import Post
register = template.Library()


def latest_post(context, num):
    latest_posts = Post.objects.all()[:num].select_related()
    return {
        'latest_posts': latest_posts
    }


register.inclusion_tag('chama/tags/latest_post.html',
                       takes_context=True)(latest_post)
