from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from app.models import Dependence, UserMail, DocumentType


class TestDependenceViews(TestCase):

    def setUp(self):
        self.dependence = Dependence.objects.create(active=True,
                                                    name='Dependence 1')
        self.client, self.user_admin, self.allow_user_admin = \
            get_authenticated_client()
        self.list_url = reverse('dependences')
        self.create_url = reverse('dependences_create')
        self.update_url = reverse('dependences_update',
                                  args=[self.dependence.id])
        self.disable_url = reverse('dependences_update_active',
                                   args=[self.dependence.id])

    def test_get_dependences(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dependence/list.html')

    def test_create_dependence(self):
        response = self.client.post(self.create_url, {
            'name': 'Test dependencia',
        })
        self.assertEquals(response.status_code, 302)

    def test_update_dependence(self):
        name = self.dependence.name
        response = self.client.post(self.update_url, {
            'name': 'Dependencia 2',
        })
        self.assertEquals(response.status_code, 302)
        self.dependence = Dependence.objects.get(id=self.dependence.id)
        self.assertNotEquals(self.dependence.name, name)


class TestDocumentTypeViews(TestCase):

    def setUp(self):
        self.document_type = DocumentType.objects.create(
            name='Tipo de documento 1',
            days_validity=12,
            active=True
        )
        self.client, self.user_admin, self.allow_user_admin = \
            get_authenticated_client()
        self.list_url = reverse('documents_type')
        self.create_url = reverse('documents_type_create')
        self.update_url = reverse('documents_type_update',
                                  args=[self.document_type.id])
        self.disable_url = reverse('documents_type_update_active',
                                   args=[self.document_type.id])

    def test_get_document_type(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'document_type/list.html')

    def test_create_document_type(self):
        dependence = Dependence.objects.create(
            name='Dependence 3',
        )
        response = self.client.post(self.create_url, {
            'name': 'Tipo de documento 2',
            'days_validity': 30,
            'active': False,
            'dependence': dependence.id,
        })
        self.assertEquals(response.status_code, 302)

    def test_update_document_type(self):
        dependence = Dependence.objects.create(
            name='Dependence 4',
        )
        name = self.document_type.name
        response = self.client.post(self.update_url, {
            'name': 'Tipo de documento 3',
            'days_validity': 5,
            'active': True,
            'dependence': dependence.id,
        })
        self.assertEquals(response.status_code, 302)
        self.document_type = DocumentType.objects.get(id=self.document_type.id)
        self.assertNotEquals(self.document_type.name, name)


class TestUserMailViews(TestCase):

    def setUp(self):
        self.client, self.user_admin, self.allow_user_admin = \
            get_authenticated_client()
        self.list_url = reverse('allowed_users')
        self.create_url = reverse('allowed_user_create')
        self.update_url = reverse('allowed_user_update',
                                  args=[self.allow_user_admin.id])
        self.disable_url = reverse('allowed_user_update_active',
                                   args=[self.allow_user_admin.id])

    def test_get_user_mail(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'allowed_user/list.html')

    def test_create_user_mail(self):
        response = self.client.post(self.create_url, {
            'email': 'test@ufps.edu.co',
            'role': 1,
            'active': True,
        })
        self.assertEquals(response.status_code, 302)

    def test_update_user_mail(self):
        active = self.allow_user_admin.active
        response = self.client.post(self.update_url, {
            'email': 'deniseduardoig@ufps.edu.co',
            'role': 1,
            'active': False,
        })
        self.assertEquals(response.status_code, 302)
        self.allow_user_admin = UserMail.objects.get(id=self.allow_user_admin.
                                                     id)
        self.assertNotEquals(self.allow_user_admin.active, active)


def get_authenticated_client():
    client = Client()
    user_admin = User.objects.create_superuser(
        username='test_admin',
        email='deniseduardoig@ufps.edu.co',
        password='admin'
    )
    allow_user_admin = UserMail.objects.create(
        email='deniseduardoig@ufps.edu.co',
        role=1,
        active=True
    )
    client.login(username='test_admin', password='admin')
    return client, user_admin, allow_user_admin
