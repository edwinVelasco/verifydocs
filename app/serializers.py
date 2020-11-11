from rest_framework import serializers
from app.models import Document, DocumentType, DocumentTypeUserMail


class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = (
            'id', 'name', 'days_validity'
        )


class TypeDocumentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('name',)


class DocumentTypeUserMailSerializer(serializers.ModelSerializer):
    document_type = TypeDocumentUserSerializer(read_only=True)

    class Meta:
        model = DocumentTypeUserMail
        fields = ('id', 'document_type')


class DocumentSerializer(serializers.ModelSerializer):
    doc_type_user = DocumentTypeUserMailSerializer(read_only=True)

    class Meta:
        model = Document
        fields = (
            'identification_applicant', 'name_applicant', 'email_applicant',
            'expedition', 'file_original', 'token', 'hash', 'file_qr',
            'hash_qr', 'doc_type_user'
        )


class DocumentListSerializer(serializers.ModelSerializer):
    doc_type_user = DocumentTypeUserMailSerializer(read_only=True)

    class Meta:
        model = Document
        doc_type_user = DocumentTypeUserMailSerializer()
        fields = (
            'id', 'identification_applicant', 'name_applicant', 'email_applicant',
            'expedition', 'created', 'doc_type_user'
        )








