import hashlib
from datetime import datetime, timedelta
import base64
from django import forms
from django.views.generic.base import View
from django.urls.base import reverse_lazy
from urllib.parse import urlencode
from django.shortcuts import HttpResponse
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic import UpdateView, TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import InvalidPage
from django.db.models import Q
from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from app.forms import VerifyDocsForm, DependenceForm, UserMailForm
from app.forms import UserMailSearchForm, DependenceSearchForm
from app.forms import DocumentTypeSearchForm, DocumentTypeForm
from app.forms import DocumentSearchForm, DocumentTypeQRForm, DocumentForm
from app.forms import DocumentTypeUserMailForm, DocumentSearchAdminForm

from app.serializers import DocumentSerializer, DocumentTypeUserMailSerializer
from app.serializers import DocumentListSerializer

from app.models import DocumentType, Dependence, UserMail, Document, \
    VerificationRequest
from app.models import DocumentTypeUserMail

# Create your views here.
from tools.PDFTools import PDFTools
from tools.mail import send_email
from verifydocs.parameters import WEB_CLIENT_URL

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


class IndexView(CreateView):
    template_name = 'index.html'
    form_class = VerifyDocsForm

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            try:
                if form.files and form.files.get('file'):
                    file = form.files.get('file')
                    from security.app import SecurityApp
                    # hash_token1 = SecurityApp(None).create_hash_256_qr(
                    #     file.file.read())
                    hash_token = PDFTools(0, 0).get_hash_document(
                        file, form.instance.verifier_email)
                    document = Document.objects.get(hash_qr=hash_token)
                else:
                    document = Document.objects.get(
                        token=form.data.get('code')).all()
            except Exception as e:
                document = None
            if not document:
                messages.error(request, 'No se ha encontrado documento')
                return render(request, self.template_name,
                              {'user': request.user, 'form': form})
            if document.expiration and document.expiration < datetime.now():
                messages.error(request, 'El documento ya expiró')
                return render(request, self.template_name,
                              {'user': request.user, 'form': form})
            form.instance.document = document
            current_date = datetime.now()
            value_token = '{}{}'.format(datetime.now().strftime(
                "%d/%m/%Y, %H:%M:%S"), form.instance.verifier_name)
            form.instance.token = hashlib.md5(value_token.encode()).\
                hexdigest()
            form.instance.end_validate_time = current_date + timedelta(
                days=1)
            form.save()
            token = f'{WEB_CLIENT_URL}/verify/{form.instance.token}'
            document_name = form.instance.document.doc_type_user.\
                document_type.name
            end_validation = form.instance.end_validate_time.\
                strftime("%m/%d/%Y, %H:%M:%S")
            send_email([form.instance.verifier_email],
                       'Solicitud de verificación aprobada',
                       {
                           'verifier_name': form.instance.verifier_name,
                           'document_name': document_name,
                           'url_token': token,
                           'end_validation': end_validation,
                       }, 'mail/email_request.html')
            applicant_name = form.instance.document.name_applicant
            send_email([form.instance.document.email_applicant],
                       'Notificación VerifyDocs',
                       {
                           'applicant_name': applicant_name,
                           'document_name': document_name,
                           'verifier_name': form.instance.verifier_name,
                       }, 'mail/email_owner.html')
            messages.success(request, 'Se ha enviado un correo electrónico '
                                      'con un enlace para que realice la '
                                      'verificación del documento.')
            return render(request, self.template_name,
                          {'user': request.user,
                           'form': VerifyDocsForm()})
        else:
            messages.error(self.request, 'Código no registrado')
            return render(request, self.template_name, {'user': request.user,
                                                        'form': form})


class VerifyView(DetailView):
    template_name = 'verify/verify.html'
    model = VerificationRequest
    slug_field = 'token'
    slug_url_kwarg = 'token'

    def get_context_data(self, **kwargs):
        context = super(VerifyView, self).get_context_data(**kwargs)
        pdf = self.object.document.file_original
        context['file'] = base64.b64encode(pdf.file.file.read()).decode()
        context['file2'] = PDFTools(0, 0, None).add_watermark(pdf.file.file)
        context['valid_token'] = self.object.end_validate_time < datetime.now()
        return context


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
                self.request.GET.get('is_active', '') == '':
            return self.model.objects.all()
        params = dict()
        if 'is_active' in self.request.GET:
            params['active'] = True
        try:
            if self.request.GET.get('name', '') != '':
                params['name__icontains'] = self.request.GET.get('name', '')
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


class DocumentTypeSettingQRView(UserAdminMixin, UpdateView):
    model = DocumentType
    template_name = 'document_type/setting_qr.html'
    form_class = DocumentTypeQRForm

    def get_success_url(self):
        messages.success(self.request,
                         'Tipo de documento actualizado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                  'documents_type')


class DocumentTypeSettingQRPreviewView(UserAdminMixin, View):
    model = DocumentType
    template_name = 'document_type/setting_qr.html'
    form_class = DocumentTypeQRForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES)
        default_file = None
        if form.is_valid():
            if form.files.get('file_u'):
                default_file = form.files.get('file_u').file
            response = HttpResponse(content_type='application/pdf')
            pdf = PDFTools(form.instance.pos_x, form.instance.pos_y,
                           form.instance.scale).\
                generate_pdf_blanck(default_file)
            response.write(pdf)
            return response
        else:
            if form.files.get('file'):
                default_file = form.files.get('file').file
            response = HttpResponse(content_type='application/pdf')
            response[
                'Content-Disposition'] = 'attachment; filename=example.pdf'
            pdf = PDFTools(form.instance.pos_x, form.instance.pos_y,
                           form.instance.scale).\
                generate_pdf_blanck(default_file)
            response.write(pdf)
            return response
        # return render(request, self.template_name, {'form': form})


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
        user = self.model.objects.last()
        user.password = ''
        user.save()
        messages.success(self.request,
                         'Usuario registrado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                   'allowed_users')

    def form_valid(self, form):
        data_post = {
            'encoding': 'utf-8',
            'csrfmiddlewaretoken': self.request.POST['csrfmiddlewaretoken'],
            'email': self.request.POST['email'],
            'role': self.request.POST['role'],
            'active': self.request.POST['active'],
            'document_types': self.request.POST.get('document_types', []),
            'password': '12345678'
        }
        password = self.request.POST['password']
        if password:
            try:
                u = User.objects.get(username=self.request.POST['email'])
                u.set_password(password)
                u.save()
            except User.DoesNotExist:
                user = User.objects.create_user(data_post['email'], data_post['email'],
                                                password=password).save()

        form_extra = UserMailForm(data=data_post)
        if form_extra.is_valid():
            return super(UserMailCreateView, self).form_valid(form_extra)
        return super(UserMailCreateView, self).form_valid(form)


class UserMailUpdateView(UserAdminMixin, UpdateView):
    model = UserMail
    template_name = 'allowed_user/create.html'
    form_class = UserMailForm

    def get_success_url(self):
        user = self.get_object()
        user.password = ''
        user.save()
        messages.success(self.request,
                         'Usuario actualizado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                   'allowed_users')

    def form_valid(self, form):
        usermail = self.get_object()
        data_post = {
            'encoding': 'utf-8',
            'csrfmiddlewaretoken': self.request.POST['csrfmiddlewaretoken'],
            'email': self.request.POST['email'],
            'role': self.request.POST['role'],
            'active': self.request.POST['active'],
            'password': '12345678'
        }
        password = self.request.POST['password']
        try:
            user = User.objects.get(username=usermail.email)
            if password:
                user.set_password(password)
            if usermail.email != self.request.POST['email']:
                user.username = self.request.POST['email']
                user.email = self.request.POST['email']
                user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(data_post['email'],
                                            data_post['email'],
                                            password=password).save()
        form_extra = UserMailForm(data=data_post)
        if form_extra.is_valid():
            return super(UserMailUpdateView, self).form_valid(form_extra)
        return super(UserMailUpdateView, self).form_valid(form)


class UserMailListView(UserAdminMixin, ListView):
    model = UserMail
    template_name = 'allowed_user/list.html'
    context_object_name = 'allowed_users_list'
    paginate_by = 5

    def get_queryset(self):
        # clear_data_session(self.request, 'filter')
        load_data_session(self.request, self.request.GET, 'filter')
        if self.request.GET.get('email', '') == '' and \
                self.request.GET.get('role', '') == '' and \
                self.request.GET.get('is_active', '') == '':
            return self.model.objects.all()
        params = dict()
        if 'is_active' in self.request.GET:
            params['active'] = True
        try:
            if self.request.GET.get('email', '') != '':
                params['email__icontains'] = self.request.GET.get('email', '')
            if self.request.GET.get('role', '') != '':
                params['role'] = self.request.GET.get('role', '')
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


class DocumentTypeUserMailView(UserAdminMixin, TemplateView):
    model = DocumentTypeUserMail
    template_name = 'allowed_user/docs_type.html'
    form_class = DocumentTypeUserMailForm

    def get_context_data(self, **kwargs):
        useremail = UserMail.objects.get(id=kwargs.get('user'))
        list_docs_type = self.model.objects.filter(usermail=useremail)
        context = super(DocumentTypeUserMailView,
                        self).get_context_data(**kwargs)
        context['list_docs_type'] = list_docs_type
        context['form'] = self.form_class()
        context['usermail'] = kwargs.get('user')
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request,
                             'Tipo de documento asociado correctamente')
        else:
            if '__all__' in form.errors:
                messages.warning(
                    self.request,
                    'El tipo de documento ya se encuentra asociado')
        return redirect(reverse_lazy('allowed_user_docs_type',
                                     args=(self.kwargs['user'],)))


class DocumentTypeUserMailActiveView(UserAdminMixin, UpdateView):
    model = DocumentTypeUserMail

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.update_active()
        messages.success(self.request,
                         'El Tipo de documento para el usuario ha sido '
                         'actualizado')
        return redirect(reverse_lazy('allowed_user_docs_type',
                                     args=(self.kwargs['user'],)))


class DocumentListView(UserMixin, ListView):
    model = Document
    template_name = 'document_home/list.html'
    context_object_name = 'document_list'
    paginate_by = 5

    def get_queryset(self):
        # clear_data_session(self.request, 'filter')
        load_data_session(self.request, self.request.GET, 'filter')
        if self.request.GET.get('id', '') == '' and \
                self.request.GET.get('doc_type_user', '') == '' and \
                self.request.GET.get('is_active', '') == '' and \
                self.request.GET.get('applicant', '') == '' and \
                self.request.GET.get('expedition', '') == '':
            return self.model.objects.all()
        params = dict()
        if 'is_enable' in self.request.GET:
            params['enable'] = True
        try:
            docs = None
            if self.request.GET.get('applicant', '') != '':
                docs = self.model.objects.filter(
                    Q(name_applicant__icontains=self.request.GET.get(
                        'applicant', '')) |
                    Q(identification_applicant__icontains=self.request.GET.get(
                        'applicant', '')) |
                    Q(email_applicant__icontains=self.request.GET.get(
                        'applicant', ''))
                )
            if self.request.GET.get('expedition', '') != '':
                # '2020-11-05'
                date = self.request.GET['expedition'].split('/')
                params['expedition__day'] = int(date[0])
                params['expedition__month'] = int(date[1])
                params['expedition__year'] = int(date[2])

            if self.request.GET.get('id', '') != '':
                params['id'] = self.request.GET.get('id', '')
            if self.request.GET.get('doc_type_user', '') != '':
                params['doc_type_user_id'] = int(self.request.GET.get(
                    'doc_type_user', ''))
            if docs:
                return docs.filter(**params)
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
        context = super(DocumentListView, self) \
            .get_context_data(**kwargs)
        context['form_search'] = DocumentSearchForm(data=self.request.GET)
        user_email = UserMail.objects.get(email=self.request.user.email)
        context['form_search'].fields['doc_type_user'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={'class': 'form-control'}
            ),
            queryset=DocumentTypeUserMail.objects.filter(usermail=user_email),
            empty_label='Seleccione tipo de documento'
        )
        context['paginator_params'] = self.get_params_pagination()
        return context

    def get_params_pagination(self):
        params = ""
        for key in self.request.GET:
            if self.request.GET[key] != '' and key != 'page':
                params += "&" + key + "=" + self.request.GET[key]
        return params


class DocumentAdminListView(UserAdminMixin, ListView):
    model = Document
    template_name = 'document_admin/list.html'
    context_object_name = 'document_list'
    paginate_by = 5

    def get_queryset(self):
        # clear_data_session(self.request, 'filter')
        load_data_session(self.request, self.request.GET, 'filter')
        if self.request.GET.get('id', '') == '' and \
                self.request.GET.get('document_type', '') == '' and \
                self.request.GET.get('is_active', '') == '' and \
                self.request.GET.get('applicant', '') == '' and \
                self.request.GET.get('expedition', '') == '':
            return self.model.objects.all()
        params = dict()
        if 'is_enable' in self.request.GET:
            params['enable'] = True
        try:
            docs = None
            if self.request.GET.get('applicant', '') != '':
                docs = self.model.objects.filter(
                    Q(name_applicant__icontains=self.request.GET.get(
                        'applicant', '')) |
                    Q(identification_applicant__icontains=self.request.GET.get(
                        'applicant', '')) |
                    Q(email_applicant__icontains=self.request.GET.get(
                        'applicant', ''))
                )
            if self.request.GET.get('expedition', '') != '':
                # '2020-11-05'
                date = self.request.GET['expedition'].split('/')
                params['expedition__day'] = int(date[0])
                params['expedition__month'] = int(date[1])
                params['expedition__year'] = int(date[2])

            if self.request.GET.get('id', '') != '':
                params['id'] = self.request.GET.get('id', '')
            if self.request.GET.get('document_type', '') != '':
                params['doc_type_user__document_type_id'] = int(self.request.GET.get(
                    'document_type', ''))
            if docs:
                return docs.filter(**params)
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
        context = super(DocumentAdminListView, self) \
            .get_context_data(**kwargs)
        context['form_search'] = DocumentSearchAdminForm(data=self.request.GET)
        context['paginator_params'] = self.get_params_pagination()
        return context

    def get_params_pagination(self):
        params = ""
        for key in self.request.GET:
            if self.request.GET[key] != '' and key != 'page':
                params += "&" + key + "=" + self.request.GET[key]
        return params


class DocumentActiveView(UserAdminMixin, UpdateView):
    model = Document

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs['pk'])
        obj.update_active()
        messages.success(self.request,
                         f'Usuario {obj} ha sido actualizado')
        return redirect(get_url_to_redirect(self.request, 'filter',
                                            'documents_admin'))


class DocumentCreateView(UserMixin, CreateView):
    model = Document
    template_name = 'document_home/create.html'
    form_class = DocumentForm

    def get_success_url(self):
        doc = self.model.objects.last()
        messages.success(self.request,
                         f'Documento con ID {doc.id} registrado correctamente')
        return get_url_to_redirect(self.request, 'filter',
                                   'documents_home')

    def get_context_data(self, **kwargs):
        user_email = UserMail.objects.filter(email=self.request.user.email,
                                             active=True).last()
        context = super(DocumentCreateView, self).get_context_data(**kwargs)
        context['form'].fields['doc_type_user'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={'class': 'form-control'}
            ),
            queryset=DocumentTypeUserMail.objects.filter(usermail=user_email,
                                                         active=True),
            empty_label='Seleccione tipo de documento'
        )
        return context

    def form_valid(self, form):
        data_post = {
            'encoding': 'utf-8',
            'csrfmiddlewaretoken': self.request.POST['csrfmiddlewaretoken'],
            'identification_applicant': self.request.POST['identification_applicant'],
            'name_applicant': self.request.POST['name_applicant'],
            'email_applicant': self.request.POST['email_applicant'],
            'expedition': self.request.POST['expedition'],
            'doc_type_user': self.request.POST['doc_type_user']
        }
        doc_type_user = DocumentTypeUserMail.objects.get(
            id=int(data_post['doc_type_user']))
        if doc_type_user.document_type.days_validity:
            data_post['expiration'] = form.instance.expedition + timedelta(
                doc_type_user.document_type.days_validity)
        files = dict()
        if 'file_original' in self.request.FILES:
            files['file_original'] = self.request.FILES['file_original']

            pdf_tool = PDFTools(pos_x=doc_type_user.document_type.pos_x,
                                pos_y=doc_type_user.document_type.pos_y,
                                scale=doc_type_user.document_type.scale)
            out_file, sha_256, token = pdf_tool.create_main_qr(
                file_doc=self.request.FILES['file_original'],
                user=self.request.user.id)

            data_post['token'] = token
            data_post['hash'] = sha_256
            data_post['hash_qr'], _ = pdf_tool.create_hash_qr(
                file_doc=out_file, user=self.request.user.id)

            files['file_qr'] = out_file
            form_extra = DocumentForm(data=data_post, files=files)
            if form_extra.is_valid():
                return super(DocumentCreateView, self).form_valid(form_extra)

        messages.error(self.request,
                         'El documento ya se encuantra registrado')
        return render(self.request, self.template_name, {'user': self.request.user,
                                                         'form': form})
        # return redirect(reverse_lazy('document_create'), form=form)

# --------------------------------- Applications ------------------------------


class TypeDocumentAplicationView(generics.ListAPIView):
    serializer_class = DocumentTypeUserMailSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        user_email = UserMail.objects.filter(email=request.user.email,
                                             active=True).last()
        serializer = self.serializer_class(
            DocumentTypeUserMail.objects.filter(usermail=user_email,
                                                active=True), many=True)
        return Response(serializer.data)


class DocumentCreateApplicationView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):
        data_post = {
            'identification_applicant': request.data[
                'identification_applicant'],
            'name_applicant': request.data['name_applicant'],
            'email_applicant': request.data['email_applicant'],
            'expedition': request.data['expedition'],
            'doc_type_user': request.data['doc_type_user']
        }
        user_email = UserMail.objects.filter(email=request.user.email).last()
        doc_type_user = DocumentTypeUserMail.objects.get(
            id=int(data_post['doc_type_user']))
        if doc_type_user.document_type.days_validity:
            data_post['expiration'] = self.get_object().expedition + timedelta(
                doc_type_user.document_type.days_validity)
        doc_types_user = DocumentTypeUserMail.objects.filter(
            usermail=user_email, active=True)
        if not doc_type_user in doc_types_user:
            return Response(
                dict(error='No tiene permiso para registrar este tipo '
                           'de documento'),
                status=status.HTTP_400_BAD_REQUEST)

        if 'file_original' in request.data:
            data_post['file_original'] = request.data['file_original']
            pdf_tool = PDFTools(pos_x=doc_type_user.document_type.pos_x,
                                pos_y=doc_type_user.document_type.pos_y,
                                scale=doc_type_user.document_type.scale)
            out_file, sha_256, token = pdf_tool.create_main_qr(
                file_doc=self.request.FILES['file_original'],
                user=self.request.user.id)

            data_post['token'] = token
            data_post['hash'] = sha_256
            data_post['hash_qr'], file = pdf_tool.create_hash_qr(
                file_doc=out_file, user=self.request.user.id)
            data_post['file_qr'] = out_file

            serializer = self.serializer_class(data=data_post)
            if serializer.is_valid():
                serializer.save()
                response = HttpResponse(status=status.HTTP_201_CREATED,
                                        content_type='application/pdf')
                response['mimetype'] = 'application/pdf'
                response['Content-Disposition'] = f'attachment; filename={out_file}'

                response.write(file)
                return response
            if 'file_original' in serializer.errors:
                return Response(dict(error='El archivo en PDF es requrido'),
                                status=status.HTTP_400_BAD_REQUEST)
            if 'token' in serializer.errors or 'hash_qr' in serializer.errors:
                return Response(
                    dict(error='El archivo ya se encuentra registrado'),
                    status=status.HTTP_400_BAD_REQUEST)
        return Response(dict(error='No se encuentra el archivo PDF'),
                        status=status.HTTP_400_BAD_REQUEST)


class DocumentListApplicationView(generics.ListAPIView):
    serializer_class = DocumentListSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request, *args, **kwargs):
        user_email = UserMail.objects.get(email=request.user.email)
        doc_types_user = DocumentTypeUserMail.objects.filter(
            usermail=user_email)
        docs = Document.objects.filter(doc_type_user__in=doc_types_user)
        serializer = self.serializer_class(
            docs, many=True)
        return Response(serializer.data)


class LogoutApplicationView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response('Cierre correcto', status=status.HTTP_200_OK)


class LoginApplicationTestPostmanView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'access_token': token.key})


class DownloadFileApplicationView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            document = Document.objects.get(id=kwargs.get('pk'))
            doc_type = document.doc_type_user.document_type
            pdf_tool = PDFTools(pos_x=doc_type.pos_x, pos_y=doc_type.pos_y,
                                scale=doc_type.scale)
            _, file = pdf_tool.create_hash_qr(
                file_doc=document.file_qr, user=request.user.id)
            response = HttpResponse(status=status.HTTP_201_CREATED,
                                    content_type='application/pdf')
            response['mimetype'] = 'application/pdf'
            response['Content-Disposition'] = f'attachment; filename={document.file_original}'
            response.write(file)
            return response
        except Document.DoesNotExist:
            return Response(dict(error='No se encuentra el archivo PDF'),
                            status=status.HTTP_400_BAD_REQUEST)


