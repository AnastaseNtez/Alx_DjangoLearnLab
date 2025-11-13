from django.urls import path
from . import views

urlpatterns = [
    # Mappings for permission testing views
    path('books/', views.book_list_view, name='book_list'),
    path('books/create/', views.book_create_view, name='book_create'),
    path('books/edit/<int:book_id>/', views.book_edit_view, name='book_edit'),
    path('books/delete/<int:book_id>/', views.book_delete_view, name='book_delete'),
    # NEW: URL for the secure form example (Name: 'form_submit')
    path('form/submit/', views.form_submit_view, name='form_submit'),
]