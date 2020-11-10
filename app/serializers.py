from rest_framework import serializers
from app.models import Document, DocumentType


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'identification_applicant', 'name_applicant', 'email_applicant',
            'expedition', 'file_original', 'document_type', 'user_mail',
            'token', 'hash', 'file_qr', 'hash_qr'
        )


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'identification_applicant', 'name_applicant', 'email_applicant',
            'expedition', 'created', 'document_type', 'file_qr'
        )


class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = (
            'id', 'name', 'days_validity'
        )





