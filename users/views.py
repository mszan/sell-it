# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django_registration.backends.activation.views import RegistrationView
from rest_framework import permissions, viewsets

from offers.models import Category, Offer
from offers.views import get_offer_thumbnail
from .forms import UserRegisterForm, UserLoginForm, UserProfileEditForm, UserEditForm
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer


def login_view(request):
    """
    View used to display user login form on GET and login user on POST.
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'You have successfully logged in!')
                return redirect('offers-home')
        else:
            username = form.cleaned_data.get('username')
            # If user account is not active, display message.
            if not User.objects.get(username=username).is_active:
                messages.warning(request, f'Account is not activated. Please check your email inbox.')
            # Else display another message.
            else:
                messages.warning(request, f'Invalid username or password.')

    else:
        form = UserLoginForm()
    return render(request, 'users/login_form.html', {'form': form})


class UserRegisterView(RegistrationView):
    """
    View used to display user register form on GET and register user on POST.
    """

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(status=1)
        return context

    def post(self, request, *args, **kwargs):
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            self.create_inactive_user(user_register_form)
            messages.success(request, f'Confirmation link has been sent to your email address.')
            return redirect('users-registration-complete')
        else:
            messages.info(request, f'Something went wrong. Account could not be created.')
            return redirect('users-register')

    def get(self, request, *args, **kwargs):
        user_register_form = UserRegisterForm()
        return render(request, 'django_registration/registration_form.html', {'user_register_form': user_register_form})


class UserProfileView(ListView):
    """
    View that displays users profile.
    """
    model = Offer
    template_name = 'users/user_details.html'
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        offers = Offer.objects.filter(owner_id=user.id, status=1).values()
        for offer in offers:
            offer['thumbnail'] = get_offer_thumbnail(offer['id'])
        return offers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        user_profile = get_object_or_404(UserProfile, user=user)
        context['user_profile'] = user_profile
        context['page_title'] = f'{user} - profile'
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    View used to change logged-in user password.
    """
    def get_success_url(self):
        return reverse_lazy('user-edit', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Changing password went wrong, try again.")
        return redirect('user-edit', pk=self.request.user.id)


class UserPasswordResetView(PasswordResetView):
    """
    View used to reset user password in case it's lost.
    """
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'

    def get_success_url(self):
        return reverse_lazy('offers-home')

    def form_valid(self, form):
        messages.success(self.request, "Check your email inbox for futher instructions.")
        return super().form_valid(form)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    View used to set new password
    when user is allowed to set a one.
    """
    template_name = 'users/password_reset_confirm.html'

    def get_success_url(self):
        return reverse_lazy('users-login')

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully. You can now log in.")
        return super().form_valid(form)


class UserProfileEditView(LoginRequiredMixin, DetailView):
    """
    View used to edit profile details and user's password.
    """
    model = UserProfile
    template_name = 'users/user_edit.html'

    def get(self, request, *args, **kwargs):
        user_instance = get_object_or_404(User, id=self.kwargs.get('pk'))
        if user_instance != self.request.user:
            messages.warning(request, 'You are not allowed to edit this profile.')
            return redirect('offers-home')
        user_edit_form = UserEditForm(instance=user_instance)

        user_profile_instance = get_object_or_404(UserProfile, user_id=self.kwargs.get('pk'))
        user_profile_edit_form = UserProfileEditForm(instance=user_profile_instance)

        user_password_reset_form = PasswordChangeForm(request.user)
        context = {
            'user_edit_form': user_edit_form,
            'user_profile_edit_form': user_profile_edit_form,
            'user_password_reset_form': user_password_reset_form,
            'profile_user': user_profile_instance.user,
            'page_title': f'{user_profile_instance.user} - edit profile'}
        return render(request, 'users/user_edit.html', context)

    def post(self, request, *args, **kwargs):
        user_instance = get_object_or_404(User, id=self.kwargs.get('pk'))
        if user_instance != self.request.user:
            messages.warning(request, 'You are not allowed to edit this profile.')
            return redirect('offers-home')
        user_edit_form = UserEditForm(request.POST, instance=user_instance)

        user_profile_instance = get_object_or_404(UserProfile, user_id=self.kwargs.get('pk'))
        user_profile_edit_form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile_instance)

        if user_edit_form.is_valid() and user_profile_edit_form.is_valid():
            user_edit_form.save()

            if request.FILES.get('profile_picture', None) is not None:
                user_profile_edit_form.save()
            else:
                user_profile = user_profile_edit_form.save(commit=False)
                user_profile.profile_picture = UserProfile.objects.get(user=request.user).profile_picture
                user_profile_edit_form.save()

            messages.success(request, f'Profile has been updated. It may take a while to take apply new profile picture.')
            return redirect('user-edit', pk=user_profile_instance.user_id)
        else:
            messages.info(request, f'Form is invalid, profile could not be updated.')
            return redirect('user-edit', pk=user_profile_instance.user_id)


class UserSetDefaultPicture(LoginRequiredMixin, TemplateView):
    """
    View used to set user's default profile picture.
    """
    template_name = 'offers/base.html'

    def post(self, request, *args, **kwargs):
        default_picture = UserProfile._meta.get_field('profile_picture').get_default()
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.profile_picture = default_picture
        user_profile.save()
        messages.success(request, 'Profile picture set to default. It may take a while to take apply changes.')
        return redirect('user-edit', pk=request.user.id)


# API views.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
