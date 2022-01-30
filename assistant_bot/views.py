from django.shortcuts import render
from .models import AddressBook
from django.urls import reverse_lazy
from django.db.models import Q
# Create your views here.

from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView

from django.contrib.auth.views import LoginView, login_required, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('homepage')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterPage, self).get_context_data(**kwargs)
        print(context)
        return context

    def form_invalid(self, form):
        messages.success(self.request, 'Your password is too common!')
        return super(RegisterPage, self).form_invalid(form)
        

class HomePage(TemplateView):
    template_name = 'homepage.html'


class AddressBookCreate(CreateView):
    model = AddressBook
    fields = ['name', 'surname', 'phone', 'email', 'street']
    template_name = 'addressbook_add.html'
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddressBookCreate, self).form_valid(form)


class AddressBookView(LoginRequiredMixin, ListView):
    model = AddressBook
    template_name = 'addressbook_listview.html'
    context_object_name = 'contacts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AddressBookView, self).get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area')
        context['contacts'] = context['contacts'].filter(user=self.request.user)
        if search_input:
            context['contacts'] = context['contacts'].filter(Q(name__startswith=search_input)|Q(surname__startswith=search_input))

        return context


@login_required
def delete_addressbook(response, pk):
    model = AddressBook.objects.filter(id=pk)
    model.delete()
    return render(response, 'addressbook_listview.html', {'contacts': AddressBook.objects.filter(user=response.user)})


class AddressBookUpdate(LoginRequiredMixin, UpdateView):
    model = AddressBook
    template_name = 'addressbook_update.html'
    context_object_name = 'contact'
    fields = ['name', 'surname', 'phone', 'email', 'street']
    success_url = reverse_lazy('contacts')


class AddressBookDetail(LoginRequiredMixin, DetailView):
    model = AddressBook
    template_name = 'addressbook_detailview.html'
    context_object_name = 'contact'
