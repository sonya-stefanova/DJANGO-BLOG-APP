from django import template
from django.db.models import Count

from blog_app.blog.models import Category, Tag, Articles

register=template.Library()

@register.simple_tag(name="categories")
def display_all_categories():
    return Category.objects.all()


@register.simple_tag(name="tags")
def display_all_tags():
    return Tag.objects.all()


@register.simple_tag(name="most_popular_articles")
def most_popular_articles():
    return Articles.objects.order_by('-clicked_times')[:4]


@register.simple_tag
def related_articles(article, num_related=3):
    # Get related articles from the same category
    related_articles = article.category.articles.exclude(id=article.id).annotate(like_count=Count('likes')).order_by('-like_count')[:num_related]
    return related_articles