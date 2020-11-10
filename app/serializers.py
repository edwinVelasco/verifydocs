from rest_framework import serializers
from app.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'identification_applicant', 'name_applicant', 'email_applicant',
            'expedition', 'file_original', 'document_type', 'user_mail',
            'token', 'hash', 'file_qr', 'hash_qr'
        )