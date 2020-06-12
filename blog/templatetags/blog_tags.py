from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe 
import markdown
# buliding custom template tag for blog app
register = template.Library()

@register.simple_tag
#retrieve total post published in the blog
def total_posts():
    return Post.published.count()
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish') [:count]
    return {'latest_posts': latest_posts}
# aggregate number of comments for a post and group in 5
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                total_comments=Count('comments')
            ).order_by('-total_comments') [:count]
@register.filter(name='markdown') #register template filters for markdown
def markdown_format(text):#template tag for markdown
    return mark_safe(markdown.markdown(text)) 