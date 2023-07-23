from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Reservation
from django.urls import reverse

# Create your tests here.

class ViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.book1 = Book.objects.create(title='Book 1', author='Author 1')
        self.book2 = Book.objects.create(title='Book 2', author='Author 2')

        self.reservation = Reservation.objects.create(book=self.book1, user=self.user,
                                                      start_date='2023-07-01', end_date='2023-07-05')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['books'], [repr(self.book1), repr(self.book2)], ordered=False)

    def test_book_search_view(self):
        response = self.client.get(reverse('book_search'), {'q': 'Book 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book 1')
        self.assertNotContains(response, 'Book 2')

    def test_book_detail_view(self):
        response = self.client.get(reverse('book_detail', args=[self.book1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['book'], self.book1)

    def test_reserve_book_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('reserve_book', args=[self.book2.pk]), {
            'start_date': '2023-07-10',
            'end_date': '2023-07-15'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Reservation.objects.filter(book=self.book2, user=self.user).exists())

    def test_user_reservations_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book 1')
        self.assertNotContains(response, 'Book 2')

    def test_all_reservations_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('all_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book 1')
        self.assertNotContains(response, 'Book 2')

    def test_edit_reservation_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_reservation', args=[self.reservation.pk]), {
            'start_date': '2023-07-06',
            'end_date': '2023-07-09'
        })
        self.assertEqual(response.status_code, 302)  # Check if it redirects after editing
        edited_reservation = Reservation.objects.get(pk=self.reservation.pk)
        self.assertEqual(edited_reservation.start_date.strftime('%Y-%m-%d'), '2023-07-06')
        self.assertEqual(edited_reservation.end_date.strftime('%Y-%m-%d'), '2023-07-09')

    

    
    