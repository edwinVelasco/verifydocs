from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from rest_framework.authtoken import views

from app.views import HomeView, IndexView, AdminHomeView, \
    DocumentAdminListView, DocumentActiveView, VerifyView
from app.views import DocumentTypeSettingQRView, DependenceListView
from app.views import DocumentTypeListView, DocumentTypeCreateView
from app.views import DocumentTypeUpdateActiveView, DocumentTypeUpdateView
from app.views import DependenceCreateView, DependenceUpdateView
from app.views import UserMailUpdateView, UserMailListView, UserMailCreateView
from app.views import UserMailActiveView, DocumentListView, DocumentCreateView
from app.views import DocumentTypeSettingQRPreviewView, DependenceActiveView
from app.views import DocumentCreateApplicationView, LogoutApplicationView
from app.views import TypeDocumentAplicationView, DocumentListApplicationView
from app.views import LoginApplicationTestPostmanView
from app.views import DownloadFileApplicationView, DocumentTypeUserMailView
from app.views import DocumentTypeUserMailActiveView


urlpatterns = [
    path('', IndexView.as_view(),
         name='index'),
    path('verify/<str:token>/', VerifyView.as_view(), name='verify'),
    path('home/', HomeView.as_view(), name='home'),
    # admin
    path('home/admin/', AdminHomeView.as_view(), name='admon'),

    # documents_type
    path('home/documents_type/', DocumentTypeListView.as_view(),
         name='documents_type'),
    path('home/documents_type/create/', DocumentTypeCreateView.as_view(),
         name='documents_type_create'),
    path('home/documents_type/<int:pk>/update/',
         DocumentTypeUpdateView.as_view(),
         name='documents_type_update'),
    path('home/documents_type/<int:pk>/setting_qr/',
         DocumentTypeSettingQRView.as_view(),
         name='documents_type_setting_qr'),
    path('home/documents_type/<int:pk>/setting_qr_preview/',
         DocumentTypeSettingQRPreviewView.as_view(),
         name='documents_type_setting_qr_preview'),
    path('home/documents_type/<int:pk>/active/',
         DocumentTypeUpdateActiveView.as_view(),
         name='documents_type_update_active'),
    # dependences
    path('home/dependences/', DependenceListView.as_view(),
         name='dependences'),
    path('home/dependences/create/', DependenceCreateView.as_view(),
         name='dependences_create'),
    path('home/dependences/<int:pk>/update/',
         DependenceUpdateView.as_view(),
         name='dependences_update'),
    path('home/dependences/<int:pk>/active/',
         DependenceActiveView.as_view(),
         name='dependences_update_active'),
    # allowed users
    path('home/allowed_users/', UserMailListView.as_view(),
         name='allowed_users'),
    path('home/allowed_users/create/', UserMailCreateView.as_view(),
         name='allowed_user_create'),
    path('home/allowed_users/<int:pk>/update/',
         UserMailUpdateView.as_view(),
         name='allowed_user_update'),
    path('home/allowed_users/<int:pk>/active/',
         UserMailActiveView.as_view(),
         name='allowed_user_update_active'),
    path('home/allowed_users/<int:user>/documet_types/',
         DocumentTypeUserMailView.as_view(),
         name='allowed_user_docs_type'),
    path('home/allowed_users/<int:user>/documet_types/<int:pk>/active/',
         DocumentTypeUserMailActiveView.as_view(),
         name='allowed_user_docs_type_active'),


    # logout_then_login
    path('logout/', LogoutView.as_view(), name='logout'),

    # documents
    # administrador
    path('home/documents_admin/', DocumentAdminListView.as_view(),
         name='documents_admin'),
    path('documents/admin/<int:pk>/active/', DocumentActiveView.as_view(),
         name='documents_update_active'),
    # administrativos
    path('documents/', DocumentListView.as_view(), name='documents_home'),
    path('document_create/', DocumentCreateView.as_view(),
         name='document_create'),

    # aplications v1
    path('aplication/v1/login/', views.obtain_auth_token),
    path('aplication/v1/login_t/', LoginApplicationTestPostmanView.as_view(),
         name='login_rest'),
    path('aplication/v1/logout/', LogoutApplicationView.as_view(),
         name='logout_rest'),

    path('application/v1/type_document_list/',
         TypeDocumentAplicationView.as_view(), name='list_document_type_rest'),
    path('application/v1/document_create/',
         DocumentCreateApplicationView.as_view(),
         name='create_document _rest'),
    path('application/v1/document_list/',
         DocumentListApplicationView.as_view(), name='list_document_rest'),
    path('application/v1/document/<int:pk>/download/',
         DownloadFileApplicationView.as_view(), name=''),

]