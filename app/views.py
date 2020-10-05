from django.shortcuts import render
from django.views.generic.base import View
from django.urls.base import reverse_lazy
from django.shortcuts import redirect, HttpResponse, render
from django.views.generic import CreateView, ListView, DeleteView
from django.views.generic import UpdateView, TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from app.forms import VerifyDocsForm
# Create your views here.

from .mixins import UserAdminMixin


class HomeView(UserAdminMixin, View):
    template = 'home.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, 'No ha iniciado sesión')
            return redirect(reverse('index'))

        context = super(HomeView, self).get_context_data(**kwargs)
        if 'is_admin' in context and context['is_admin']:
            return redirect(reverse('admon'))

        if 'is_valid' in context and not context['is_valid']:
            messages.error(self.request,
                           'Su usuario no tienen acceso al sistema')
            return redirect(reverse('logout'))

        return render(request, self.template, {'user': request.user})


class AdminHomeView(UserAdminMixin, View):
    template = 'admin.html'

    def get(self, request, *args, **kwargs):
        context = super(AdminHomeView, self).get_context_data(**kwargs)
        if not 'is_admin' in context and not context['is_admin']:
            return redirect(reverse('index'))

        return render(request, self.template, {'user': request.user})


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        contest = self.get_context_data()
        contest['form'] = VerifyDocsForm()
        return self.render_to_response(contest)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = VerifyDocsForm(data=request.POST)
        if form.is_valid():
            messages.success(request, 'Formulario correcto')
            return render(request, self.template_name, {'user': request.user,
                                                        'form': form})
        else:
            messages.error(self.request, 'Codigo no registrado')
            return render(request, self.template_name, {'user': request.user,
                                                        'form': form})


