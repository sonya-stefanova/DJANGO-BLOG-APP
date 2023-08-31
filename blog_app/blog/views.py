from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin

from blog_app.blog.forms import CreateArticleForm, UpdateArticleForm, CreateCommentForm
from blog_app.blog.models import Articles, Category, Tag

UserModel = get_user_model()


class HomePageListView(ListView):
    template_name = "blog/index.html"
    model = Articles
    paginate_by = 3

    def get_queryset(self):
        return Articles.objects.filter(admin_approved=True).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider'] = Articles.objects.filter(admin_approved=True, home_slider=True)

        return context


class ArticleDetailsView(DetailView, FormMixin):
    '''
    This is a detail view of the article including:
    - the article content and other attributes;
    - comments;
    - next/previous functionality
    '''
    template_name = "blog/article_details.html"
    model = Articles
    context_object_name = "article"
    form_class = CreateCommentForm

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        article.clicked_times += 1
        article.save()

        return article


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_article = self.object
        context['form'] = self.get_form()

        try:
            context['next_article'] = Articles.objects.filter(created_on__gt=current_article.created_on).order_by(
                'created_on').first()
        except Articles.DoesNotExist:
            context['next_article'] = None

        try:
            context['previous_article'] = Articles.objects.filter(created_on__lt=current_article.created_on).order_by(
                '-created_on').first()
        except Articles.DoesNotExist:
            context['previous_article'] = None

        context['author_profile'] = current_article.author.profile  # This line might be causing the issue

        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.article = self.object
            form.save()
            return super().form_valid(form)
        else:
            return super().form_invalid()

    def get_success_url(self):
        return reverse_lazy('details_article', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            self.form_valid(form)

        return self.form_valid(form)

class CategoryListView(ListView):
    template_name ="categories/articles_list_per_category.html"
    model = Articles
    paginate_by = 3

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Articles.objects.filter(admin_approved=True, category=self.category).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        articles = Articles.objects.filter(admin_approved=True, category=self.category).order_by('-pk')
        context['articles'] = articles
        context['category'] = self.category
        return context

class TagsListView(ListView):
    model = Articles
    template_name = 'tags/list_tagged_posts.html'
    success_url = reverse_lazy('home')
    paginate_by = 3

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Articles.objects.filter(admin_approved=True, tag=self.tag).order_by('-pk')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        articles = Articles.objects.filter(admin_approved=True, tag=self.tag).order_by('-pk')
        context['articles'] = articles
        context['tag'] = self.tag
        return context


@method_decorator(login_required(login_url='home'), name='dispatch')
class CreateArticleView(SuccessMessageMixin, CreateView):
    model = Articles
    template_name = 'blog/create_article.html'
    form_class = CreateArticleForm
    success_message = 'Your article has been submitted for review successfully'

    def form_valid(self, form):
        #the article author is set to the currently authenticated user
        form.instance.author = self.request.user

        # Save the instance of the article submission with admin_approved False
        form.instance.admin_approved = False

        # Save the article instance
        article = form.save()

        # Extract the value of the Tag input from the submitted form data and split it
        # into a list of tags using commas as separators.
        tags = self.request.POST.get('tag').split(',')

        # Clear existing tags and add each tag to the article's tags.
        for tag in tags:
            current_tag, created = Tag.objects.get_or_create(title=tag.strip())
            article.tag.add(current_tag)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details_article', kwargs={"slug": self.object.slug})




@method_decorator(login_required(login_url='home'), name='dispatch')
class UpdateArticleView(SuccessMessageMixin, UpdateView):
    model = Articles
    template_name = 'blog/update_article.html'
    form_class = UpdateArticleForm
    success_message = "Your article has been successfully edited."

    def get_success_url(self):
        return reverse_lazy('details_article', kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.admin_approved = False

        tags = form.cleaned_data.get('tags')

        if tags:
            # If tags we need to split the tags by comma and strip whitespace
            tags = [tag.strip() for tag in tags.split(',')]
            # Then, remove empty tags
            tags = [tag for tag in tags if tag]

            # Next, clear existing tags
            form.instance.tag.clear()
            #and add the updated tags. If not existing, they will be created with the get or create  built in function
            for tag in tags:
                current_tag, created = Tag.objects.get_or_create(title=tag)
                self.object.tag.add(current_tag)

        return super().form_valid(form)

    #Only the author can change articles
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        '''This method retrieves the object article
        that this view is supposed to work with. 
        The retrieved object is then stored in self.object 
        so that it can be used later in the view.
        '''

        if self.object.author != self.request.user:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)

class DeleteArticleView(DeleteView):
    model = Articles
    success_url = reverse_lazy('home')
    template_name = 'blog/delete_article.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            self.object.delete()
        else:
            return HttpResponseRedirect('self.success_url')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)

class SearchView(ListView):
    model = Articles
    template_name = 'blog/search.html'
    paginate_by = 3

    def get_queryset(self):
        search_query = self.request.GET.get("q", None)

        if search_query:
            # Use Q objects to perform a case-insensitive search on multiple fields
            queryset = Articles.objects.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tag__title__icontains=search_query),
                admin_approved=True
            ).order_by('-created_on').distinct()
            return queryset

        return Articles.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("q", "")
        return context

class WriteForUsView(TemplateView):
    template_name = 'blog/write_for_us.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



def favorite_post(request, slug):
    article = get_object_or_404(Articles, slug=slug, admin_approved=True)
    user = request.user

    if article.favourited_by.filter(pk=user.pk).exists():
        article.favourited_by.remove(user)
    else:
        article.favourited_by.add(user)

    # Save the article after modifying the favourited_by field
    article.save()

    # Redirect to the user's profile page after updating favorites
    profile_url = reverse('details-profile', args=[user.profile.slug])
    return redirect(profile_url)


# custom 404 view
def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

#custom 500 view
def custom_500(request):
    return render(request, 'errors/500.html', status=500)


