import os
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from studio.studio import settings


# Create your models here.

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    fio = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return '%s %s %s' % (self.fio, self.login, self.email)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    photo = models.ImageField(upload_to='orders/photos', null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    status_id = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    comment = models.CharField(max_length=200, null=True)

    def save_uploaded_photo(self, uploaded_photo):
        filename = os.path.join("orders/photos", str(self.id), uploaded_photo.name)
        full_path = os.path.join(settings.MEDIA_ROOT, filename)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb') as destination:
            for chunk in uploaded_photo.chunks():
                destination.write(chunk)

        self.photo = filename

    def delete_category(self):
        self.delete()

    def __str__(self):
        return '%s %s %s' % (self.name, self.description, self.photo)


def user_registrated():
    return None
