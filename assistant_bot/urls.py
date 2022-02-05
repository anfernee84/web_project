from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import FileUploadView, HomePage, AddressBookCreate, AddressBookView, ShowFiles, delete_addressbook, AddressBookUpdate, AddressBookDetail, CustomLoginView, RegisterPage


from .views import HomePage, AddressBookCreate, AddressBookView, delete_addressbook, AddressBookUpdate, \
    AddressBookDetail, CustomLoginView, RegisterPage, show_world_news, show_finance_news, show_sport_news, \
    show_entertainment_news, show_tech_news, show_weather, currency_converter

url_patterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('add-contact/', AddressBookCreate.as_view(), name='addressbook'),
    path('view-contacts/', AddressBookView.as_view(), name='contacts'),
    path('task-delete/<int:pk>', delete_addressbook, name='delete'),
    path('task-update/<int:pk>', AddressBookUpdate.as_view(), name='update'),
    path('file/', FileUploadView, name='file'), #
    path('show-files/<slug:ext>', ShowFiles, name='show-files'), #
    path('contact-view/<int:pk>', AddressBookDetail.as_view(), name='contact'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('news/', show_world_news,  name='news'),
    path('finance/', show_finance_news, name='finance'),
    path('sport/', show_sport_news, name='sport'),
    path('entertainment/', show_entertainment_news, name='entertainment'),
    path('hacker/', show_tech_news, name='hacker'),
    path('weather/', show_weather, name='weather'),
    path('currency/', currency_converter, name='currency'),

]
