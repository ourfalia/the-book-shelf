from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('book_list', views.book_list, name='book_list'),
    path('search/', views.book_search, name='book_search'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/reserve/', views.reserve_book, name='reserve_book'),
    path('user_reservations/', views.user_reservations, name='user_reservations'),
    path('all_reservations/', views.all_reservations, name='all_reservations'), 
    path('reservation/<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),  
    path('reservation/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'), 
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'), 
]