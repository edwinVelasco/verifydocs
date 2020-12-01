import datetime
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from app.models import Dependence, UserMail, DocumentType, \
    DocumentTypeUserMail, Document, VerificationRequest
from tools.PDFTools import create_pdf


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
        self.setting_qr_url = reverse('documents_type_setting_qr',
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

    def test_setting_qr(self):
        response = self.client.post(self.setting_qr_url, {
            'pos_x': 0,
            'pos_y': 0,
            'scale': 42,
        })
        self.assertEquals(response.status_code, 302)


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
            'csrfmiddlewaretoken': 'xxx',
            'password': ''
        })
        self.assertEquals(response.status_code, 302)

    def test_update_user_mail(self):
        active = self.allow_user_admin.active
        response = self.client.post(self.update_url, {
            'email': 'deniseduardoig@ufps.edu.co',
            'role': 1,
            'active': False,
            'csrfmiddlewaretoken': 'xxx',
            'password': ''
        })
        self.assertEquals(response.status_code, 302)
        self.allow_user_admin = UserMail.objects.get(id=self.allow_user_admin.
                                                     id)
        self.assertNotEquals(self.allow_user_admin.active, active)


class TestDocumentViews(TestCase):

    def setUp(self):
        self.client, self.user, self.allowed_user = \
            get_authenticated_administrative_client()
        self.list_url = reverse('documents_home')
        self.register_url = reverse('document_create')

    def test_get_documents(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'document_home/list.html')

    def test_register_document(self):
        dependence = Dependence.objects.create(
            name='Registro y control',
            active=True
        )
        doc_type = DocumentType.objects.create(
            name= 'Terminación de materias',
            days_validity= 10,
            active= True,
            dependence=dependence,
            pos_x=100,
            pos_y=100,
            scale=63,
        )
        doc_type_user = DocumentTypeUserMail.objects.create(
            document_type=doc_type,
            usermail=self.allowed_user,
            active=True,
        )
        file = SimpleUploadedFile('file.pdf', create_pdf())
        response = self.client.post(self.register_url, data={
            'identification_applicant': '1090999888',
            'name_applicant': 'Denis González',
            'email_applicant': 'deniseduardoig@ufps.edu.co',
            'expedition': datetime.datetime.now().date(),
            'file_original': file,
            'doc_type_user': doc_type_user.id,
            'csrfmiddlewaretoken': 'xxx',
        })
        self.assertEquals(response.status_code, 302)


class TestRequestVerificationView(TestCase):

    def setUp(self):
        try:
            user = UserMail.objects.get(email='albertove@ufps.edu.co')
        except Exception:
            user = UserMail.objects.create(
                email='albertove@ufps.edu.co',
                role='2',
                active=True,
            )
        dependence = Dependence.objects.create(
            name='Credito y cartera',
            active=True
        )
        doc_type = DocumentType.objects.create(
            name='Certificado de notas',
            days_validity=10,
            active=True,
            dependence=dependence,
            pos_x=100,
            pos_y=100,
            scale=63,
        )
        doc_type_user = DocumentTypeUserMail.objects.create(
            document_type=doc_type,
            usermail=user,
            active=True,
        )
        file = SimpleUploadedFile('file.pdf', create_pdf('request document'))
        self.document = Document.objects.create(
            identification_applicant='1090888999',
            name_applicant='Denis González',
            email_applicant='deniseduardoig@ufps.edu.co',
            expedition=datetime.datetime.now().date(),
            file_original=file,
            token='A'*32,
            hash='B'*64,
            hash_qr='C'*64,
            expiration=datetime.datetime.now()+timedelta(days=30),
            file_qr=file,
            doc_type_user=doc_type_user,
            enable=True,
        )
        self.client = Client()
        self.request_verification_url = reverse('index')
        verification = VerificationRequest.objects.create(
            verifier_name='DENIS',
            verifier_email='deniseduardoig@ufps.edu.co',
            token='X'*32,
            document=self.document,
            end_validate_time=datetime.datetime.now()+timedelta(days=1),
        )
        self.verification = reverse('verify', args=[verification.token])

    def test_request_verification(self):
        response = self.client.post(self.request_verification_url, data={
            'verifier_name': 'DENIS AC',
            'verifier_email': 'deniseduardoisidrogonzalez@gmail.com',
            'verifier_email_two': 'deniseduardoisidrogonzalez@gmail.com',
            'code': 'A'*32
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(VerificationRequest.objects.filter(
            verifier_name='DENIS AC').all()) > 0, True)

    def test_verification(self):
        response = self.client.get(self.verification)
        self.assertEquals(response.status_code, 200)


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


def get_authenticated_administrative_client():
    client = Client()
    user = User.objects.create_user(
        username='test_user',
        email='albertove@ufps.udes.edu.co',
        password='user'
    )
    allowed_user = UserMail.objects.create(
        email='albertove@ufps.udes.edu.co',
        role=2,
        active=True
    )
    client.login(username='test_user', password='user')
    return client, user, allowed_user