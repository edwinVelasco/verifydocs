from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from app.views import HomeView, IndexView, AdminHomeView
from app.views import DocumentTypeListView, DocumentTypeCreateView
from app.views import DocumentTypeUpdateActiveView, DocumentTypeUpdateView

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
    path('home/documents_type/<int:pk>/active/',
         DocumentTypeUpdateActiveView.as_view(),
         name='documents_type_update_active'),


    # logout_then_login
    path('logout/', LogoutView.as_view(), name='logout'),

]