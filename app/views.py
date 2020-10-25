from django.shortcuts import render
from django.views.generic.base import View
from django.urls.base import reverse_lazy
from django.urls import reverse as urls_reverse
from urllib.parse import urlencode
from django.shortcuts import redirect, HttpResponse, render
from django.views.generic import CreateView, ListView, DeleteView
from django.views.generic import UpdateView, TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import Http404
from django.utils.translation import gettext as _

from app.forms import VerifyDocsForm, DependenceForm, UserMailForm, \
    UserMailSearchForm, DependenceSearchForm
from app.models import DocumentType, Dependence, UserMail
from app.forms import DocumentTypeSearchForm, DocumentTypeForm
# Create your views here.

from .mixins import UserAdminMixin, UserMixin


def load_data_session(request, params, data):
    request.session[data] = params


def clear_data_session(request, data):
    if data in request.session:
        del request.session[data]


def there_is_data(request, data):
    return data in request.session and request.session[data]


def get_url_to_redirect(request, data, url_data):
    # url = urls_reverse(url_data)
    url = reverse_lazy(url_data)
    if there_is_data(request, data):
        query_string = urlencode(request.session[data])
        url = f'{url}?{query_string}'
        return url
    clear_data_session(request, data)
    return url


class HomeView(UserMixin, View):
    template = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'user': request.user})


class AdminHomeView(UserAdminMixin, View):
    template = 'admin.html'

    def get(self, request, *args, **kwargs):
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


class DependenceCreateView(UserAdminMixin, CreateView):
    model = Dependence
    template_name = 'dependence/create.html'
    form_class = DependenceForm

    def get_success_url(self):
        messages.success(self.request,
                         'Dependencia registrado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                   'dependences')


class DependenceUpdateView(UserAdminMixin, UpdateView):
    model = Dependence
    template_name = 'dependence/create.html'
    form_class = DependenceForm

    def get_success_url(self):
        messages.success(self.request,
                         'Dependencia actualizado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                   'dependences')


class DependenceListView(UserAdminMixin, ListView):
    model = Dependence
    template_name = 'dependence/list.html'
    context_object_name = 'dependence_list'
    paginate_by = 5

    def get_queryset(self):
        # clear_data_session(self.request, 'filter')
        load_data_session(self.request, self.request.GET, 'filter')
        if self.request.GET.get('name', '') == '' and \
                self.request.GET.get('acronym', '') == '' and \
                self.request.GET.get('is_active', '') == '':
            return self.model.objects.all()
        params = dict()
        if 'is_active' in self.request.GET:
            params['active'] = True
        try:
            if self.request.GET.get('name', '') != '':
                params['name__icontains'] = self.request.GET.get('name', '')
            if self.request.GET.get('acronym', '') != '':
                params['acronym__icontains'] = self.request.GET.get('acronym',
                                                                    '')
            return self.model.objects.filter(**params)
        except ValueError:
            return self.model.objects.all()

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, self.paginate_by, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(
            page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(
                    "Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            if page.number < page_number:
                page = paginator.page(page_number - 1)
                return (
                paginator, page, page.object_list, page.has_other_pages())
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            page = paginator.page(page_number - 1)
            return (paginator, page, page.object_list, page.has_other_pages())

    def get_context_data(self, **kwargs):
        context = super(DependenceListView, self) \
            .get_context_data(**kwargs)
        context['form_search'] = DependenceSearchForm(data=self.request.GET)
        context['paginator_params'] = self.get_params_pagination()
        return context

    def get_params_pagination(self):
        params = ""
        for key in self.request.GET:
            if self.request.GET[key] != '' and key != 'page':
                params += "&" + key + "=" + self.request.GET[key]
        return params


class DependenceActiveView(UserAdminMixin, UpdateView):
    model = Dependence

    def get(self, request, *args, **kwargs):
        doc_type = self.model.objects.get(id=kwargs['pk'])
        doc_type.update_active()
        messages.success(self.request,
                         f'Dependencia {doc_type} ha sido actualizado')
        return redirect(get_url_to_redirect(self.request, 'filter',
                                            'dependences'))


class DocumentTypeListView(UserAdminMixin, ListView):
    model = DocumentType
    template_name = 'document_type/list.html'
    context_object_name = 'document_type_list'
    paginate_by = 10

    def get_queryset(self):
        # clear_data_session(self.request, 'filter')
        load_data_session(self.request, self.request.GET, 'filter')
        if self.request.GET.get('name', '') == '' and \
                self.request.GET.get('dependence', '') == '' and \
                self.request.GET.get('is_active', '') == '':
            return self.model.objects.all()
        params = dict()
        if 'is_active' in self.request.GET:
            params['active'] = True
        try:
            if self.request.GET.get('name', '') != '':
                params['name__icontains'] = self.request.GET.get('name', '')
            if self.request.GET.get('dependence', '') != '':
                params['dependence_id'] = self.request.GET.get('dependence',
                                                              '')
            return self.model.objects.filter(**params)
        except ValueError:
            return self.model.objects.all()

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, self.paginate_by, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(
            page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(
                    "Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            if page.number < page_number:
                page = paginator.page(page_number-1)
                return (paginator, page, page.object_list, page.has_other_pages())
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            page = paginator.page(page_number-1)
            return (paginator, page, page.object_list, page.has_other_pages())

    def get_context_data(self, **kwargs):
        context = super(DocumentTypeListView, self)\
            .get_context_data(**kwargs)
        context['form_search'] = DocumentTypeSearchForm(data=self.request.GET)
        context['paginator_params'] = self.get_params_pagination()
        return context

    def get_params_pagination(self):
        params = ""
        for key in self.request.GET:
            if self.request.GET[key] != '' and key != 'page':
                params += "&" + key + "=" + self.request.GET[key]
        return params


class DocumentTypeCreateView(UserAdminMixin, CreateView):
    model = DocumentType
    template_name = 'document_type/create.html'
    form_class = DocumentTypeForm

    def get_success_url(self):
        messages.success(self.request, 'Tipo de documento registrado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                   'documents_type')


class DocumentTypeUpdateView(UserAdminMixin, UpdateView):
    model = DocumentType
    template_name = 'document_type/create.html'
    form_class = DocumentTypeForm

    def get_success_url(self):
        messages.success(self.request,
                         'Tipo de documento actualizado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                  'documents_type')


class DocumentTypeUpdateActiveView(UserAdminMixin, TemplateView):
    model = DocumentType

    def get(self, request, *args, **kwargs):
        doc_type = self.model.objects.get(id=kwargs['pk'])
        doc_type.update_active()
        messages.success(self.request,
                         f'Tipo de documento {doc_type} ha sido actualizado')
        return redirect(get_url_to_redirect(self.request, 'filter',
                                   'documents_type'))


class UserMailCreateView(UserAdminMixin, CreateView):
    model = UserMail
    template_name = 'allowed_user/create.html'
    form_class = UserMailForm

    def get_success_url(self):
        messages.success(self.request,
                         'Usuario registrado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                   'allowed_users')


class UserMailUpdateView(UserAdminMixin, UpdateView):
    model = UserMail
    template_name = 'allowed_user/create.html'
    form_class = UserMailForm

    def get_success_url(self):
        messages.success(self.request,
                         'Usuario actualizado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                   'allowed_users')


class UserMailListView(UserAdminMixin, ListView):
    model = UserMail
    template_name = 'allowed_user/list.html'
    context_object_name = 'allowed_users_list'
    paginate_by = 5

    def get_queryset(self):
        # clear_data_session(self.request, 'filter')
        load_data_session(self.request, self.request.GET, 'filter')
        if self.request.GET.get('email', '') == '' and \
                self.request.GET.get('dependence', '') == '' and \
                self.request.GET.get('is_staff', '') == '' and \
                self.request.GET.get('is_active', '') == '':
            return self.model.objects.all()
        params = dict()
        if 'is_staff' in self.request.GET:
            params['is_staff'] = True
        if 'is_active' in self.request.GET:
            params['active'] = True
        try:
            if self.request.GET.get('email', '') != '':
                params['email__icontains'] = self.request.GET.get('email', '')
            if self.request.GET.get('dependence', '') != '':
                params['dependence'] = self.request.GET.get('dependence', '')
            return self.model.objects.filter(**params)
        except ValueError:
            return self.model.objects.all()

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, self.paginate_by, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(
            page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(
                    "Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            if page.number < page_number:
                page = paginator.page(page_number - 1)
                return (
                paginator, page, page.object_list, page.has_other_pages())
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            page = paginator.page(page_number - 1)
            return (paginator, page, page.object_list, page.has_other_pages())

    def get_context_data(self, **kwargs):
        context = super(UserMailListView, self) \
            .get_context_data(**kwargs)
        context['form_search'] = UserMailSearchForm(data=self.request.GET)
        context['paginator_params'] = self.get_params_pagination()
        return context

    def get_params_pagination(self):
        params = ""
        for key in self.request.GET:
            if self.request.GET[key] != '' and key != 'page':
                params += "&" + key + "=" + self.request.GET[key]
        return params


class UserMailActiveView(UserAdminMixin, UpdateView):
    model = UserMail

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs['pk'])
        obj.update_active()
        messages.success(self.request,
                         f'Usuario {obj} ha sido actualizado')
        return redirect(get_url_to_redirect(self.request, 'filter',
                                            'allowed_users'))

