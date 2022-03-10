from django.db.models import fields
from rest_framework import serializers
from .models import Company, ModelHolder


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'registration_id']


class ModelHolderSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = ModelHolder
        fields = '__all__'
