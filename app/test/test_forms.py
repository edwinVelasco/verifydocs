from django.test import TestCase
from app.forms import DependenceForm, DocumentTypeForm, UserMailForm
from app.models import Dependence


class TestDependenceForm(TestCase):

    def test_dependence_form_valid(self):
        form = DependenceForm(data={
            'name': 'Dependencia 1',
            'active': True,
        })
        self.assertTrue(form.is_valid())


class TestDocumentTypeForm(TestCase):

    def test_document_type_form_valid(self):
        dependence = Dependence.objects.create(
            name='Dependencia 1'
        )
        form = DocumentTypeForm(data={
            'name': 'Tipo de documento 1',
            'days_validity': 40,
            'active': True,
            'dependence': dependence.id,
        })
        self.assertTrue(form.is_valid())


class TestUserMailForm(TestCase):

    def test_user_mail_form(self):
        form = UserMailForm(data={
            'email': 'deniseduardoig@ufps.edu.co',
            'role': 1,
            'active': False,
        })
        self.assertTrue(form.is_valid())
