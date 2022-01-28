from django.shortcuts import render
from .models import AddressBook
from django.urls import reverse_lazy
# Create your views here.

from django.views.generic import TemplateView, CreateView, ListView


class HomePage(TemplateView):
    template_name = 'homepage.html'


class AddressBookCreate(CreateView):
    model = AddressBook
    fields = '__all__'
    template_name = 'addressbook_add.html'
    success_url = reverse_lazy('homepage')


class AddressBookView(ListView):
    model = AddressBook
    template_name = 'addressbook_listview.html'
    context_object_name = 'contacts'
