from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views, logout

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"),
         name='index'),
    path('home/', TemplateView.as_view(template_name="home.html"),
         name='home'),
    # logout_then_login
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), {'next_page': '/'},
         name='logout'),

]