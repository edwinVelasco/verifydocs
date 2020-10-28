from django.test import SimpleTestCase
from django.urls import resolve, reverse
from app.views import IndexView, HomeView, AdminHomeView, \
    DocumentTypeListView, DocumentTypeCreateView, DocumentTypeUpdateView, \
    DocumentTypeUpdateActiveView, DependenceListView, \
    DependenceCreateView, DependenceUpdateView, DependenceActiveView, \
    UserMailListView, UserMailCreateView, UserMailUpdateView, \
    UserMailActiveView
from django.contrib.auth.views import LogoutView


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func.view_class, IndexView)

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomeView)

    def test_admon_url_resolves(self):
        url = reverse('admon')
        self.assertEquals(resolve(url).func.view_class, AdminHomeView)

    def test_documents_type_url_resolves(self):
        url = reverse('documents_type')
        self.assertEquals(resolve(url).func.view_class, DocumentTypeListView)

    def test_documents_type_create_url_resolves(self):
        url = reverse('documents_type_create')
        self.assertEquals(resolve(url).func.view_class, DocumentTypeCreateView)

    def test_documents_type_update_url_resolves(self):
        url = reverse('documents_type_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, DocumentTypeUpdateView)

    def test_documents_type_update_active_url_resolves(self):
        url = reverse('documents_type_update_active', args=[1])
        self.assertEquals(resolve(url).func.view_class,
                          DocumentTypeUpdateActiveView)

    def test_dependences_url_resolves(self):
        url = reverse('dependences')
        self.assertEquals(resolve(url).func.view_class, DependenceListView)

    def test_dependences_create_url_resolves(self):
        url = reverse('dependences_create')
        self.assertEquals(resolve(url).func.view_class, DependenceCreateView)

    def test_dependences_update_url_resolves(self):
        url = reverse('dependences_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, DependenceUpdateView)

    def test_dependences_update_active_url_resolves(self):
        url = reverse('dependences_update_active', args=[1])
        self.assertEquals(resolve(url).func.view_class, DependenceActiveView)

    def test_allowed_users_url_resolves(self):
        url = reverse('allowed_users')
        self.assertEquals(resolve(url).func.view_class, UserMailListView)

    def test_allowed_user_create_url_resolves(self):
        url = reverse('allowed_user_create')
        self.assertEquals(resolve(url).func.view_class, UserMailCreateView)

    def test_allowed_user_update_url_resolves(self):
        url = reverse('allowed_user_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, UserMailUpdateView)

    def test_allowed_user_update_active_url_resolves(self):
        url = reverse('allowed_user_update_active', args=[1])
        self.assertEquals(resolve(url).func.view_class, UserMailActiveView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)
