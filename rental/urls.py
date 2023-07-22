from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('book_list', views.book_list, name='book_list'),
    path('search/', views.book_search, name='book_search'),
]