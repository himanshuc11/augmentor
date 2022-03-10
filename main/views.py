from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from rest_framework.parsers import FileUploadParser

from rest_framework.serializers import Serializer, FileField


from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from django.contrib.auth import logout

from .models import Company, ModelHolder
import cloudinary
import cloudinary.uploader
import cloudinary.api

from .serializers import CompanySerializer, ModelHolderSerializer


# Create your views here.
class SignUpView(APIView):
    def post(self, request):
        try:
            data = {}
            serializer = CompanySerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                account.save()
                token = Token.objects.get_or_create(user=account)[0].key
                data["message"] = "user registered successfully"
                data["company"] = account.company_name
                data["token"] = token
            else:
                data = serializer.errors
            return Response(data)
        except IntegrityError as e:
            account = Company.objects.get(username='')
            account.delete()
            raise ValidationError({"400": f'{str(e)}'})
        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            company = Company.objects.filter(
                company_name=data['company_name'])[0]
        except Company.DoesNotExist:
            return Response('Invalid Email ID')

        if company.check_password(data['password']):
            token = Token.objects.get_or_create(
                user=company)
            (tokenData, _) = token
            print(vars(tokenData))
            return Response({"token": tokenData.key})
        else:
            return Response('Please enter correct password')


class LogoutAPIView(APIView):
    def post(self, request):
        if request.user.is_anonymous:
            return Response('You are already logged out')
        request.user.auth_token.delete()
        logout(request)
        return Response('Logged Out')


class CRUDView(APIView):
    def get(self, request):
        data = ModelHolder.objects.all()
        serializer = ModelHolderSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_file = request.FILES['file']
        url = cloudinary.uploader.upload(user_file, resource_type="image")
        name = request.data['name']
        model = ModelHolder(name=name, company=Company.objects.get(
            company_name="root"), gltf_url=url['secure_url'])
        model.save()
        return Response(url['secure_url'])
