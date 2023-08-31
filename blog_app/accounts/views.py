from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators import cache
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import BlogAppUserCreationForm, BlogAppPasswordChangeForm, ProfileUpdateForm, CustomSignInForm
from django.contrib.auth import views as auth_views, login, get_user_model
from django.views import generic as views, generic
from django.urls import reverse_lazy, reverse
from django.core.cache import cache

from .models import Profile, BlogAppUser
from ..blog.models import Articles


UserModel = get_user_model()

class SignUpView(SuccessMessageMixin,views.CreateView):
    template_name = 'accounts/sign-up.html'
    form_class = BlogAppUserCreationForm
    success_url = reverse_lazy('home')
    success_message = "You are now signed up! Get awesome experience in our blog!"

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if context is to redirect to the page where the user started off
        # context['next'] = self.request.GET.get('next', '')
        return context

    def get_success_url(self):
        return self.request.POST.get('next', self.success_url)


class SignInView(auth_views.LoginView):
    template_name = 'accounts/sing-in.html'
    form_class = CustomSignInForm


class SignOutView(SuccessMessageMixin, auth_views.LogoutView):
    template_name = 'accounts/sign-out.html'
    success_message = 'You are now signed out'

    # https://github.com/SilviyaKolchakova/trip_app/blob/main/templates/accounts/login_page.html
@method_decorator(login_required(login_url='sign-in'), name='dispatch')
class UserPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/change-password.html'
    success_url = reverse_lazy('password-change-done')
    form_class = BlogAppPasswordChangeForm

    def form_valid(self, form):
        # Save the new password and perform any other actions if necessary
        form.save()

        # Render the password change confirmation template directly
        return render(self.request, 'accounts/change-password-done.html')


@method_decorator(login_required(login_url='sign-in'), name='dispatch')
class ProfileUpdateView(SuccessMessageMixin, views.UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/update_profile.html'
    success_message = 'You have successfully updated your profile!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details-profile', kwargs={'slug': self.object.slug})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProfileView(generic.ListView):
    template_name = 'accounts/profile.html'
    context_object_name = 'user_articles'
    paginate_by = 3

    def get_queryset(self):
        logged_in_user = self.request.user
        favorited_articles = Articles.objects.filter(admin_approved=True, favourited_by=logged_in_user)
        authored_articles = Articles.objects.filter(admin_approved=True, author=logged_in_user)

        # Combine both sets of articles
        user_articles = favorited_articles | authored_articles

        # Order the articles by their ID in descending order
        user_articles = user_articles.order_by('-id')

        return user_articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = self.request.user.profile
        context['authored_articles'] = Articles.objects.filter(admin_approved=True, author=self.request.user)
        context['favorited_articles'] = Articles.objects.filter(admin_approved=True, favourited_by=self.request.user)

        return context
class ArticlesByAuthorUserView(ListView):
    template_name = 'accounts/author-articles.html'
    model = Articles
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        author = get_object_or_404(BlogAppUser, profile__slug=slug)
        context['author'] = author
        context['articles'] = Articles.objects.filter(author=author, admin_approved=True)
        return context

# @method_decorator(cache_page(60 * 5), name='dispatch')
class AuthorsListView(ListView):
    template_name = 'accounts/authors-list.html'
    model = Profile
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(authored_article_count=Count('user__author_articles'))
        return queryset.filter(authored_article_count__gt=0)


