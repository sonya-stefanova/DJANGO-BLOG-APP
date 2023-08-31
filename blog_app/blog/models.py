from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from ckeditor.fields import RichTextField

UserModel = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=72, unique=True, null=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def articles_counter(self):
        return self.articles.all().count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    title=models.CharField(max_length=40)
    slug = models.SlugField(max_length=50, editable=False, unique=True, null=False, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def articles_counter(self):
        return self.articles.all().count()

class Articles(models.Model):

    title = models.CharField(max_length=175, blank=False, null=False)
    admin_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    content = RichTextField(null=True, blank=True,)
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    slug = models.SlugField(max_length=72, unique=True, null=False, blank=True)
    intro = RichTextField(null=True, blank=True,)
    clicked_times = models.PositiveIntegerField(default=0)


    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, default=1, related_name="author_articles")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='articles')

    tag = models.ManyToManyField(Tag, related_name='articles', blank=True)
    related_articles = models.ManyToManyField('self', blank=True)
    favourited_by = models.ManyToManyField(UserModel, related_name='favorite_articles', blank=True)

    home_slider = models.BooleanField(default=False, null=False, blank=False)



    def comments_counter(self):
        return self.comments.all().count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.category_id:
            # Assuming you have a specific category to use as default, replace 'default_category_title' with the desired category title.
            default_category, _ = Category.objects.get_or_create(title='Uncategorized')
            self.category = default_category

            if not self.id:  # Only set the status for new articles
                self.status = 'pending_review'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.author}'

    def article_tags(self):
        return ', '.join([tag.title for tag in self.tag.all()])

    class Meta:
        verbose_name_plural = 'Articles'
        ordering = ('-created_on',)



class Comment(models.Model):
    article = models.ForeignKey(Articles,on_delete=models.CASCADE,related_name="comments")

    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)



    def __str__(self):
        return self.article.title