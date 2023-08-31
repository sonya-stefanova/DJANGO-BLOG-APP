# urlpatterns = [
#     path('accounts/', include([
#         path('sign-up/', include([
#             path('', combined_sign_up_view, name='combined register'),
#             path('trainer/', TrainerSignUpView.as_view(), name='trainer sign up'),
#             path('trainee/', TraineeSignUpView.as_view(), name='trainee sign up'),
#         ])),
#         path('login/', SignInView.as_view(), name='log in'),
#         path('sign-out.html/', SignOutView.as_view(), name='sign out'),
#         path('update-personal/<int:pk>', UpdatePersonalView.as_view(), name='user update personal'),
#
#     ]))
# ]
from django.urls import path, reverse_lazy

from blog_app.accounts import views


urlpatterns = [
    path('authors/', views.AuthorsListView.as_view(), name='authors-list'),
    path('update-profile/<slug:slug>/', views.ProfileUpdateView.as_view(), name='update-profile'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),
    path('profile-information/<slug:slug>/', views.ProfileView.as_view(), name='details-profile'),
    path('author-articles/<slug:slug>/', views.ArticlesByAuthorUserView.as_view(), name='author-articles'),
    path('change-password/', views.UserPasswordChangeView.as_view(), name='change-password'),

]

# urlpatterns = [
#     path('register/', UserRegisterView.as_view(), name='register'),
#     path('login/', UserLoginView.as_view(), name='login user'),
#     path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
#     path('password_change_done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password_change_done'),
#     path('logout/', UserLogoutView.as_view(), name='logout user'),
#     path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
#     path('profile/delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),
#     path('profile/details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
#
# ]