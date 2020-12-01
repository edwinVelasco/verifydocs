from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse

from app.models import UserMail, DocumentTypeUserMail, DocumentType, Dependence
from tools.PDFTools import create_pdf


class TestRegisterFile(TestCase):

    def setUp(self):
        self.user_mail = UserMail.objects.create(
            email='deniseduardoig@ufps.edu.co',
            role=3,
            active=True,
            password='123',
        )
        self.user = User.objects.create(
            username='deniseduardoig@ufps.edu.co',
            email='deniseduardoig@ufps.edu.co',
        )
        self.user.set_password('123')
        dependence = Dependence.objects.create(
            name='Registro y control',
            active=True,
        )
        document_type = DocumentType.objects.create(
            name='Certificado terminación de materias',
            days_validity=30,
            active=True,
            dependence=dependence,
            pos_x=0,
            pos_y=0,
            scale=84,
        )
        self.doc_type_user = DocumentTypeUserMail.objects.create(
            document_type=document_type,
            usermail=self.user_mail,
            active=True,
        )
        self.register_url = reverse('create_document _rest')

    def test_register_document(self):
        client = APIClient()
        client.force_authenticate(self.user)
        file = SimpleUploadedFile('file.pdf', create_pdf('restfull'))
        response = client.post(self.register_url, data={
            'identification_applicant': '1090777888',
            'name_applicant': 'Eduardo González',
            'email_applicant': 'deniseduardoig@ufps.edu.co',
            'expedition': datetime.now().date(),
            'file_original': file,
            'doc_type_user': self.doc_type_user.id,
        })
        self.assertEquals(response.status_code, 201)

