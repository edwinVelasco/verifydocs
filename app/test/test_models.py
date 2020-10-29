from django.test import TestCase

from app.models import Dependence, UserMail, DocumentType


class TestDependenceModel(TestCase):

    def setUp(self):
        self.dependence = Dependence.objects.create(
            name='dependencia test',
            active=True
        )

    def test_dependence_update_active(self):
        init_value = self.dependence.active
        self.dependence.update_active()
        self.assertEquals(self.dependence.active, not init_value)


class TestUserMailModel(TestCase):

    def setUp(self):
        self.user_mail = UserMail.objects.create(
            email='deniseduardoig@ufps.edu.co',
            role=1,
            active=True,
        )

    def test_user_mail_update_active(self):
        init_value = self.user_mail.active
        self.user_mail.update_active()
        self.assertEquals(self.user_mail.active, not init_value)


class TestDocumentType(TestCase):
    
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            name='nombre de prueba de documento',
            days_validity=30,
            active=True,
        )
    
    def test_document_type_update_active(self):
        init_value = self.document_type.active
        self.document_type.update_active()
        self.assertEquals(self.document_type.active, not init_value)
