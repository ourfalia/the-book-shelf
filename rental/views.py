from django.shortcuts import render, get_object_or_404
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


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'rental/book_detail.html', {'book': book})
