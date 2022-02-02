import datetime
from re import split
from django.shortcuts import redirect
from .models import AddressBook, NoteBook
from .forms import AddAddressBook
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

    def form_invalid(self, form):
        messages.success(self.request, 'Incorrect password or login')
        return super(CustomLoginView, self).form_invalid(form)


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

    def form_invalid(self, form):
        messages.success(self.request, 'Your password is too common!')
        return super(RegisterPage, self).form_invalid(form)
        

class HomePage(TemplateView):
    template_name = 'homepage.html'


class AddressBookCreate(CreateView):
    model = AddressBook
    form_class = AddAddressBook
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
        context['contacts'] = context['contacts'].filter(user=self.request.user)
        if context['contacts']:
            context['is_empty'] = '0'

        today_date = datetime.date.today()

        search_input = self.request.GET.get('search-area')
        b_day = self.request.GET.get('b-day')
        all_input = self.request.GET.get('all')

        if search_input:
            context['contacts'] = context['contacts'].filter(Q(name__startswith=search_input)|Q(surname__startswith=search_input))
            return context

        if b_day:
            context['contacts'] = AddressBook.objects.filter(user=self.request.user, birthday__month__gte=today_date.month, birthday__month__lte=today_date.month + 1)

        if all_input is not None:
            context['contacts'] = AddressBook.objects.filter(user=self.request.user)

        return context


@login_required
def delete_addressbook(response, pk):
    model = AddressBook.objects.filter(id=pk)
    model.delete()
    return redirect('contacts')


class AddressBookUpdate(LoginRequiredMixin, UpdateView):
    model = AddressBook
    template_name = 'addressbook_update.html'
    context_object_name = 'contact'
    form_class = AddAddressBook
    success_url = reverse_lazy('contacts')


class AddressBookDetail(LoginRequiredMixin, DetailView):
    model = AddressBook
    template_name = 'addressbook_detailview.html'
    context_object_name = 'contact'


class NoteBookCreate(CreateView):
    model = NoteBook

    fields = ['title', 'description', 'tags']
    template_name = 'notebook_add.html'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        tags = form.instance.tags
        form.instance.user = self.request.user
        if tags:
            form.instance.tags = split(r'[,;+= ]', tags[0])
        return super(NoteBookCreate, self).form_valid(form)


class NoteBookDetail(LoginRequiredMixin, DetailView):
    model = NoteBook
    template_name = 'notebook_detail_view.html'
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        context = super(NoteBookDetail, self).get_context_data(**kwargs)

        return context


class NoteBookUpdate(LoginRequiredMixin, UpdateView):
    model = NoteBook
    template_name = 'notebook_update.html'
    fields = ['title', 'description', 'tags']
    success_url = reverse_lazy('notes')


class NoteBookView(LoginRequiredMixin, ListView):
    model = NoteBook
    template_name = 'notebook_listview.html'
    context_object_name = 'notes'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NoteBookView, self).get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)

        tag_set = set()
        search_input = self.request.GET.get('search-area')
        filter_tags = get_tags_from_request(self.request.GET, self.request.user)

        if filter_tags:
            context['notes'] = context['notes'].filter(tags__overlap=filter_tags)

        if search_input:
            context['notes'] = context['notes'].filter(title__contains=search_input)
            return context

        for tag_item in context['notes'].values_list('tags', flat=True).order_by('tags'):
            if tag_item:
                for tag in tag_item:
                    tag_set.add(tag)
        context['filter_tags'] = tag_set
        return context


def get_tags_from_request(get_request, user):
    all_tags = NoteBook.objects.filter(user=user).values_list('tags', flat=True)
    searched_tags = []
    for tag_item in all_tags:
        if tag_item:
            for tag in tag_item:
                if get_request.get(tag):
                    searched_tags.append(tag)
    return searched_tags


@login_required
def delete_notebook(response, pk):
    model = NoteBook.objects.filter(id=pk)
    model.delete()
    tag_set = set()
    for tag_item in NoteBook.objects.values_list('tags', flat=True).order_by('tags'):
        if tag_item:
            for tag in tag_item:
                tag_set.add(tag)
    return redirect('notes')
