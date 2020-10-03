from django.shortcuts import render
from django.views.generic.base import View
from django.urls.base import reverse_lazy
from django.shortcuts import redirect, HttpResponse, render
from django.views.generic import CreateView, ListView, DeleteView
from django.views.generic import UpdateView, TemplateView
from django.shortcuts import render, redirect, reverse
# Create your views here.


class HomeView(View):
    template = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))

        return render(request, self.template, self.get_context())


