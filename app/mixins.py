from django.views.generic.base import ContextMixin
from .models import UserMail


class UserAdminMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(UserAdminMixin, self).get_context_data(**kwargs)
        user = self.request.user
        if user and user.is_authenticated:
            if user.is_staff:
                context['is_admin'] = True
            else:
                context['is_valid'] = False
                user_email = UserMail.objects.filter(email=user.email)
                if user_email:
                    context['is_valid'] = True

        return context


