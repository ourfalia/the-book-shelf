from django.shortcuts import render
from .models import Book

# Create your views here.


def book_list(request):
    books = Book.objects.all()
    return render(request, 'rental/book_list.html', {'books': books})


def book_search(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'rental/book_list.html', {'books': books})