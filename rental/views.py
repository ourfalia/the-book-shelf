from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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


@login_required
def reserve_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        user = request.user

        if Reservation.objects.filter(book=book, start_date__lte=end_date, end_date__gte=start_date).exists():
            return render(request, 'rental/book_unavailable.html', {'book': book})

        reservation = Reservation.objects.create(book=book, user=user, start_date=start_date, end_date=end_date)
        return redirect('user_reservations')

    return render(request, 'rental/book_reserve.html', {'book': book})