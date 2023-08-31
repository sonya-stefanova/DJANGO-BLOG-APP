from django.contrib import admin
from django.utils.safestring import mark_safe

from blog_app.blog.models import Articles, Category, Tag, Comment

def approve_articles(modeladmin, request, queryset):
    queryset.update(admin_approved=True)

# Register your models here.
@admin.register(Articles)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ['created_on', 'title']
    list_display = ['title', 'created_on', 'author', 'slug', 'tags', 'admin_approved']
    search_fields =['title', 'content']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ['related_articles',]

    actions = [approve_articles]  # Add the custom action

    @staticmethod
    def tags(obj):
        return ", ".join([article.title for article in obj.tag.all()])

    def display_content(self, obj):
        return mark_safe(obj.content)

    display_content.short_description = 'Content'

@admin.register(Category)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_filter = ['title', ]
    list_display = ['title', 'slug']
    search_fields =['category']
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['name', 'email', 'article__title']
    list_display = ['name', 'email', 'created_on', 'article_title']
    search_fields = ['name', 'article__title']

    def article_title(self, obj):
        return obj.article.title

    article_title.short_description = 'Article Title'

