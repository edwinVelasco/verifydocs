from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views, logout
from app.views import HomeView, IndexView, AdminHomeView

urlpatterns = [
    path('', IndexView.as_view(),
         name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/admin/', AdminHomeView.as_view(), name='admon'),
    # logout_then_login
    path('logout/', auth_views.LogoutView.as_view(next_page='index'),
         {'next_page': '/'}, name='logout'),

]