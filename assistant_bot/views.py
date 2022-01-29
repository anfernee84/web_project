from django.shortcuts import render
from .models import AddressBook
from django.urls import reverse_lazy
from django.db.models import Q
# Create your views here.

from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView


class HomePage(TemplateView):
    template_name = 'homepage.html'


class AddressBookCreate(CreateView):
    model = AddressBook
    fields = '__all__'
    template_name = 'addressbook_add.html'
    success_url = reverse_lazy('contacts')


class AddressBookView(ListView):
    model = AddressBook
    template_name = 'addressbook_listview.html'
    context_object_name = 'contacts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AddressBookView, self).get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area')
        if search_input:
            context['contacts'] = AddressBook.objects.filter(Q(name__startswith=search_input)|Q(surname__startswith=search_input))
        return context


def delete_addressbook(response, pk):
    model = AddressBook.objects.filter(id=pk)
    model.delete()
    return render(response, 'addressbook_listview.html', {'contacts': AddressBook.objects.all()})


class AddressBookUpdate(UpdateView):
    model = AddressBook
    template_name = 'addressbook_update.html'
    context_object_name = 'contact'
    fields = '__all__'
    success_url = reverse_lazy('contacts')


class AddressBookDetail(DetailView):
    model = AddressBook
    template_name = 'addressbook_detailview.html'
    context_object_name = 'contact'
