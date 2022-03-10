from unicodedata import name
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid


class CompanyManager(BaseUserManager):
    def create_user(self, company_name, registration_id, password):
        if not company_name:
            raise ValueError('Compnay must have a company Name')
        user = self.model(
            company_name=company_name,
            registration_id=registration_id,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, company_name, registration_id, password):
        user = self.create_user(
            company_name=company_name, registration_id=registration_id, password=password)
        user.is_superuser = True
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)


# Create your models here.
class Company(AbstractBaseUser):
    company_name = models.CharField(max_length=128, unique=True)
    registration_id = models.CharField(max_length=128)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'company_name'
    REQUIRED_FIELDS = ['registration_id']
    objects = CompanyManager()

    def __str__(self):
        return str(self.company_name)

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser


class ModelHolder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Company Name-Company unique identifier
    name = models.CharField(max_length=64, unique=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="model")
    gltf_url = models.URLField(max_length=1024)

    def __str__(self):
        return str(str(self.company) + "-" + str(self.gltf_url))
