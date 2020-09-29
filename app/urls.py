from django.urls import path
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name="social_app/index.html"),
         name='social_app_login')
]