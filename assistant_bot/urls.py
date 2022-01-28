from django.urls import path
from .views import HomePage, AddressBookCreate, AddressBookView

url_patterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('add-contact/', AddressBookCreate.as_view(), name='addressbook'),
    path('view-contacts/', AddressBookView.as_view(), name='contacts')
]