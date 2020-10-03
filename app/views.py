from django.shortcuts import render
from django.views.generic.base import View
from django.urls.base import reverse_lazy
from django.shortcuts import redirect, HttpResponse, render
from django.views.generic import CreateView, ListView, DeleteView
from django.views.generic import UpdateView, TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
# Create your views here.

from .models import UserMail


class HomeView(View):
    template = 'home.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('index'))

        user_email = UserMail.objects.filter(email=request.user.email)
        if not user_email:
            messages.error(self.request, 'Su usuario no tienen acceso al sistema')
            return redirect(reverse('logout'))

        return render(request, self.template, {'user': request.user})


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = request.POST
        print(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


