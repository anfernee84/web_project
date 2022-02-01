from django.shortcuts import render
from .models import AddressBook
from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView

from django.contrib.auth.views import LoginView, login_required, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from newsapi import NewsApiClient

import json

import urllib.request

from datetime import datetime

from pycountry import countries


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
            context['contacts'] = context['contacts'].filter(
                Q(name__startswith=search_input) | Q(surname__startswith=search_input))

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


@login_required
def show_world_news(request):
    newsapi = NewsApiClient(api_key='92ee8fd958374204ada73045c7fe5936')
    top = newsapi.get_top_headlines(sources='bbc-news')

    content = top['articles']
    desc = []
    news = []
    img = []

    for i in range(len(content)):
        text = content[i]
        news.append(text['title'])
        desc.append(text['description'])
        img.append(text['urlToImage'])
    mylist = zip(news, desc, img)

    user_location = json.loads(urllib.request.urlopen('http://ipinfo.io/json').read())
    weather_url = urllib.request.urlopen(
        f"https://api.openweathermap.org/"
        f"data/2.5/weather?q={user_location['city']}&appid=206c04ecd30711b37b3e460efd0e40d7"
    ).read()
    weather_data = json.loads(weather_url)
    data = {
        'name': weather_data['name'],
        'temp_c': (weather_data['main']['temp'] - 273.15).__round__(1),
        'temp_f': ((weather_data['main']['temp'] - 273.15) * 9 / 5 + 32).__round__(1)}

    return render(request=request, template_name='news_page.html', context={'mylist': mylist, 'data': data})


@login_required
def show_finance_news(request):
    newsapi = NewsApiClient(api_key='92ee8fd958374204ada73045c7fe5936')
    top = newsapi.get_top_headlines(sources='business-insider')

    content = top['articles']
    desc = []
    news = []
    img = []

    for i in range(len(content)):
        text = content[i]
        news.append(text['title'])
        desc.append(text['description'])
        img.append(text['urlToImage'])
    mylist = zip(news, desc, img)

    user_location = json.loads(urllib.request.urlopen('http://ipinfo.io/json').read())
    weather_url = urllib.request.urlopen(
        f"https://api.openweathermap.org/"
        f"data/2.5/weather?q={user_location['city']}&appid=206c04ecd30711b37b3e460efd0e40d7"
    ).read()
    weather_data = json.loads(weather_url)
    data = {
        'name': weather_data['name'],
        'temp_c': (weather_data['main']['temp'] - 273.15).__round__(1),
        'temp_f': ((weather_data['main']['temp'] - 273.15) * 9 / 5 + 32).__round__(1)}

    return render(request=request, template_name='finance_page.html', context={'mylist': mylist, 'data': data})


@login_required()
def show_sport_news(request):
    newsapi = NewsApiClient(api_key='92ee8fd958374204ada73045c7fe5936')
    top = newsapi.get_top_headlines(sources='bbc-sport')

    content = top['articles']
    desc = []
    news = []
    img = []

    for i in range(len(content)):
        text = content[i]
        news.append(text['title'])
        desc.append(text['description'])
        img.append(text['urlToImage'])
    mylist = zip(news, desc, img)

    user_location = json.loads(urllib.request.urlopen('http://ipinfo.io/json').read())
    weather_url = urllib.request.urlopen(
        f"https://api.openweathermap.org/"
        f"data/2.5/weather?q={user_location['city']}&appid=206c04ecd30711b37b3e460efd0e40d7"
    ).read()
    weather_data = json.loads(weather_url)
    data = {
        'name': weather_data['name'],
        'temp_c': (weather_data['main']['temp'] - 273.15).__round__(1),
        'temp_f': ((weather_data['main']['temp'] - 273.15) * 9 / 5 + 32).__round__(1)}

    return render(request=request, template_name='sport_page.html', context={'mylist': mylist, 'data': data})


@login_required()
def show_entertainment_news(request):
    newsapi = NewsApiClient(api_key='92ee8fd958374204ada73045c7fe5936')
    top = newsapi.get_top_headlines(sources='buzzfeed')

    content = top['articles']
    desc = []
    news = []
    img = []

    for i in range(len(content)):
        text = content[i]
        news.append(text['title'])
        desc.append(text['description'])
        img.append(text['urlToImage'])
    mylist = zip(news, desc, img)

    user_location = json.loads(urllib.request.urlopen('http://ipinfo.io/json').read())
    weather_url = urllib.request.urlopen(
        f"https://api.openweathermap.org/"
        f"data/2.5/weather?q={user_location['city']}&appid=206c04ecd30711b37b3e460efd0e40d7"
    ).read()
    weather_data = json.loads(weather_url)
    data = {
        'name': weather_data['name'],
        'temp_c': (weather_data['main']['temp'] - 273.15).__round__(1),
        'temp_f': ((weather_data['main']['temp'] - 273.15) * 9 / 5 + 32).__round__(1)}

    return render(request=request, template_name='entertainment_page.html', context={'mylist': mylist, 'data': data})


@login_required
def show_hacker_news(request):
    newsapi = NewsApiClient(api_key='92ee8fd958374204ada73045c7fe5936')
    top = newsapi.get_top_headlines(sources='hacker-news')

    content = top['articles']
    desc = []
    news = []
    img = []

    for i in range(len(content)):
        text = content[i]
        news.append(text['title'])
        desc.append(text['description'])
        img.append(text['urlToImage'])
    mylist = zip(news, desc, img)

    user_location = json.loads(urllib.request.urlopen('http://ipinfo.io/json').read())
    weather_url = urllib.request.urlopen(
        f"https://api.openweathermap.org/"
        f"data/2.5/weather?q={user_location['city']}&appid=206c04ecd30711b37b3e460efd0e40d7"
    ).read()
    weather_data = json.loads(weather_url)
    data = {
        'name': weather_data['name'],
        'temp_c': (weather_data['main']['temp'] - 273.15).__round__(1),
        'temp_f': ((weather_data['main']['temp'] - 273.15) * 9 / 5 + 32).__round__(1)}

    return render(request=request, template_name='hacker_page.html', context={'mylist': mylist, 'data': data})


@login_required()
def show_weather(request):
    user_location = json.loads(urllib.request.urlopen('http://ipinfo.io/json').read())
    weather_url = urllib.request.urlopen(
        f"https://api.openweathermap.org/"
        f"data/2.5/weather?q={user_location['city']}&appid=206c04ecd30711b37b3e460efd0e40d7"
    ).read()
    weather_data = json.loads(weather_url)
    data = {
        'name': weather_data['name'],
        'country': countries.get(alpha_2=weather_data['sys']['country']).name,
        'temp_c': (weather_data['main']['temp'] - 273.15).__round__(1),
        'temp_f': ((weather_data['main']['temp'] - 273.15) * 9 / 5 + 32).__round__(1),
        'clouds': weather_data['clouds']['all'],
        'wind_kmh': (weather_data['wind']['speed'] * 3.6).__round__(1),
        'wind_mh': (weather_data['wind']['speed'] * 2.237).__round__(1),
        'visibility_km': (weather_data['visibility'] / 1000).__round__(1),
        'visibility_m': (weather_data['visibility'] / 1609).__round__(1),
        'pressure': weather_data['main']['pressure'],
        'humidity': weather_data['main']['humidity'],
        'dt': datetime.fromtimestamp(weather_data['dt']).ctime()
    }
    if request.method == 'POST':
        weather_url = urllib.request.urlopen(
            f"https://api.openweathermap.org/"
            f"data/2.5/weather?q={request.POST['city']}&appid=206c04ecd30711b37b3e460efd0e40d7"
        ).read()
        weather_data = json.loads(weather_url)
        data = {
            'name': weather_data['name'],
            'country': countries.get(alpha_2=weather_data['sys']['country']).name,
            'temp_c': (weather_data['main']['temp'] - 273.15).__round__(1),
            'temp_f': ((weather_data['main']['temp'] - 273.15) * 9 / 5 + 32).__round__(1),
            'clouds': weather_data['clouds']['all'],
            'wind_kmh': (weather_data['wind']['speed'] * 3.6).__round__(1),
            'wind_mh': (weather_data['wind']['speed'] * 2.237).__round__(1),
            'visibility_km': (weather_data['visibility'] / 1000).__round__(1),
            'visibility_m': (weather_data['visibility'] / 1609).__round__(1),
            'pressure': weather_data['main']['pressure'],
            'humidity': weather_data['main']['humidity'],
            'dt': datetime.fromtimestamp(weather_data['dt']).ctime()
        }
        return render(request=request, template_name='result_weather_page.html', context={'data': data})
    return render(request=request, template_name='weather_page.html', context={'data': data})
