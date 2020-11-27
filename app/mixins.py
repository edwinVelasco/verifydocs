from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from app.models import UserMail


class UserMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('index'))
        user_email = UserMail.objects.filter(email=request.user.email,
                                             active=True)
        if not user_email:
            messages.warning(request=request,
                             message=f'El correo electrónico '
                                     f'{request.user.email} no tiene acceso')
            try:
                user = User.objects.filter(email=request.user.email).last()
                user.delete()
            except User.DoesNotExist:
                pass

            return redirect(reverse('logout'))
        user_email = user_email.first()
        if user_email.role == 1:
            return redirect(reverse('admon'))

        if user_email.role == 3:
            messages.warning(request=request,
                             message=f'El correo electrónico '
                                     f'{request.user.email} no tiene acceso, '
                                     f'Es de un usuario de aplicación')
            return redirect(reverse('logout'))
        request.session['dependence'] = user_email.get_dependence_name()
        return super().dispatch(request, *args, **kwargs)


class UserAdminMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('index'))

        user_email = UserMail.objects.filter(email=request.user.email,
                                             active=True)
        if not user_email:
            messages.warning(request=request,
                             message=f'El correo electrónico "'
                                     f'{request.user.email}" no tiene acceso')
            return redirect(reverse('logout'))
        user_email = user_email.first()
        if not user_email.role == 1:
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)
