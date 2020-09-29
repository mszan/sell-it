from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic.base import TemplateView
from django_registration.backends.activation.views import ActivationView

from users.views import UserRegisterView, UserProfileView, login_view, UserProfileEditView, UserPasswordChangeView, \
    UserPasswordResetView, UserPasswordResetConfirmView, UserSetDefaultPicture

urlpatterns = [
    path("users/activate/complete/",
         TemplateView.as_view(template_name="django_registration/activation_complete.html"),
         name="django_registration_activation_complete", ),

    path("users/activate/<str:activation_key>/",
         ActivationView.as_view(), name="users-registration-activate", ),

    path("users/register/complete/",
         TemplateView.as_view(template_name="django_registration/registration_complete.html"),
         name="users-registration-complete", ),

    path("users/register/closed/",
         TemplateView.as_view(template_name="django_registration/registration_disallowed.html"),
         name="users-registration-disallowed", ),

    path('users/register/',
         UserRegisterView.as_view(),
         name='users-register'),

    path('users/login/',
         login_view,
         name='users-login'),

    path('users/logout/',
         LogoutView.as_view(),
         name='users-logout'),

    path('users/<int:pk>/',
         UserProfileView.as_view(),
         name='user-details'),

    path('users/<int:pk>/edit/',
         UserProfileEditView.as_view(),
         name='user-edit'),

    path('users/edit/user-set-default-picture/',
         UserSetDefaultPicture.as_view(),
         name='user-set-default-picture'),

    path('users/password-change/',
         UserPasswordChangeView.as_view(),
         name='user-password-change'),

    path('users/password-reset/',
         UserPasswordResetView.as_view(),
         name='user-password-reset'),

    path('users/password-reset-confirm/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(),
         name='user-password-reset-confirm'),

    path('users/', include('django.contrib.auth.urls')), ]
