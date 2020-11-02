from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from app.views import HomeView, IndexView, AdminHomeView, \
    DocumentTypeSettingQRView, DocumentTypeSettingQRPreviewView
from app.views import DocumentTypeListView, DocumentTypeCreateView, \
    DocumentTypeUpdateActiveView, DocumentTypeUpdateView, DependenceListView, \
    DependenceCreateView, DependenceUpdateView, DependenceActiveView,\
    UserMailUpdateView, UserMailListView, UserMailCreateView, \
    UserMailActiveView

urlpatterns = [
    path('', IndexView.as_view(),
         name='index'),
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


    # logout_then_login
    path('logout/', LogoutView.as_view(), name='logout'),


]