from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
import stripe

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

        today = timezone.now().date()
        if start_date < str(today) or end_date < str(today):
            return render(request, 'rental/book_unavailable.html', {'book': book})

        if Reservation.objects.filter(book=book, start_date__lte=end_date, end_date__gte=start_date).exists():
            return render(request, 'rental/book_unavailable.html', {'book': book})

        reservation = Reservation.objects.create(book=book, user=user, start_date=start_date, end_date=end_date)
        return redirect('user_reservations')

    return render(request, 'rental/book_reserve.html', {'book': book})


@login_required
def user_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user, is_checked_out=False)

    total_price = 0
    for reservation in reservations:
        
        num_days = (reservation.end_date - reservation.start_date).days + 1
        reservation.price = num_days * 3  
        total_price += reservation.price

    return render(request, 'rental/user_reservations.html', {'reservations': reservations, 'total_price': total_price})


@login_required
def all_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)

    return render(request, 'rental/all_reservations.html', {'reservations': reservations})

@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        reservation.start_date = start_date
        reservation.end_date = end_date
        reservation.save()

        return redirect('user_reservations') 

    return render(request, 'rental/edit_reservation.html', {'reservation': reservation})


@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        reservation.delete()  

        return redirect('user_reservations')  

    return render(request, 'rental/cancel_reservation.html', {'reservation': reservation})


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    user = request.user
    reservations = Reservation.objects.filter(user=user, is_checked_out=False)

    if not reservations.exists():
        return redirect('user_reservations')

    total_price = 0

    for reservation in reservations:
        num_days = (reservation.end_date - reservation.start_date).days + 1
        reservation.price = num_days * 3  
        total_price += reservation.price
        stripe_total = round(total_price * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    if request.method == 'POST':
        for reservation in reservations:
            reservation.is_checked_out = True
            reservation.save()

        return redirect('checkout_success')
    
    books = Book.objects.filter(reservation__in=reservations)

    return render(request, 'rental/checkout.html', {
        'reservations': reservations, 
        'total_price': total_price,
        'stripe_public_key': stripe_public_key, 
        'client_secret': intent.client_secret,
        'books': books,
        })
        


@login_required
def checkout_success(request):
    return render(request, 'rental/checkout_success.html')