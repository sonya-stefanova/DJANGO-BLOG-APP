from django.urls import path
from blog_app.blog.views import (
    HomePageListView,
    ArticleDetailsView,
    CategoryListView,
    TagsListView,
    CreateArticleView,
    UpdateArticleView,
    DeleteArticleView, SearchView, WriteForUsView, favorite_post
)

urlpatterns = [
    path('search-results/', SearchView.as_view(), name='search'),
    path('create-article/', CreateArticleView.as_view(), name='create_article'),
    path('update-article/<slug:slug>/', UpdateArticleView.as_view(), name='update_article'),
    path('delete-article/<slug:slug>/', DeleteArticleView.as_view(), name='delete_article'),
    path('write-for-us/', WriteForUsView.as_view(), name='write_for_us'),  # Ensure this comes before <slug:slug>/ pattern
    path('<slug:slug>/', ArticleDetailsView.as_view(), name='details_article'),
    path('home-tips/<slug:slug>/', CategoryListView.as_view(), name='details_category'),
    path('tags/<slug:slug>/', TagsListView.as_view(), name='details_tags'),
    path('', HomePageListView.as_view(), name='home'),
    path('favorite/<slug:slug>/', favorite_post, name='favorite_post'),

]
