from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AddressBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    street = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
