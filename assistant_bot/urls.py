from django.urls import path
from .views import HomePage, AddressBookCreate, AddressBookView, delete_addressbook, AddressBookUpdate, AddressBookDetail, CustomLoginView, RegisterPage, \
    NoteBookCreate, NoteBookDetail, NoteBookView, NoteBookUpdate, delete_notebook
from django.contrib.auth.views import LogoutView


url_patterns = [
    path('', HomePage.as_view(), name='homepage'),

    path('add-contact/', AddressBookCreate.as_view(), name='addressbook'),
    path('view-contacts/', AddressBookView.as_view(), name='contacts'),
    path('task-delete/<int:pk>', delete_addressbook, name='delete'),
    path('task-update/<int:pk>', AddressBookUpdate.as_view(), name='update'),
    path('contact-view/<int:pk>', AddressBookDetail.as_view(), name='contact'),

    path('note-add/', NoteBookCreate.as_view(), name='note_create'),
    path('note-view/<int:pk>', NoteBookDetail.as_view(), name='note'),
    path('view-notes/', NoteBookView.as_view(), name='notes'),
    path('note-update/<int:pk>', NoteBookUpdate.as_view(), name='note-update'),
    path('delete-note/<int:pk>', delete_notebook, name='delete_note'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register')
]
