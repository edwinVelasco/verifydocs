from django.shortcuts import redirect, reverse
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserMail


class UserMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('index'))
        user_email = UserMail.objects.filter(email=request.user.email)
        if not user_email:
            return redirect(reverse('logout'))
        if request.user.is_staff:
            return redirect(reverse('admon'))
        return super().dispatch(request, *args, **kwargs)


class UserAdminMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('index'))

        user_email = UserMail.objects.filter(email=request.user.email)
        if not user_email:
            return redirect(reverse('logout'))
        if not request.user.is_staff:
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)
