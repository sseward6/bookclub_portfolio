from django.test import TestCase, Client
from django.urls import reverse
from bookclub.models import Book, Member, Recommendation
from bookclub.serializers import BookSerializer, MemberSerializer, RecommendationSerializer, RecommendationViewSerializer
import pytest
from rest_framework import status
import json

# Create your tests here.

client = Client()

##################################################################################
# test api/member/ GET
##################################################################################

class GetAllMembersTest(TestCase):
    def setUp(self):
        Member.objects.create(name='Sam', email='sam@gmail.com')
        Member.objects.create(name='Steve', email='steve@gmail.com')
        Member.objects.create(name='Stella', email='stella@gmail.com')
        
    def test_get_all_members(self):
        response = client.get(reverse('member_list'))
        members = Member.objects.all()
        count=members.count()
        self.assertEqual(count, 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MemberSerializer(members, many=True)
        self.assertEqual(response.json(), serializer.data)


##################################################################################
# test api/member/<id> GET
##################################################################################

class GetSingleMembersTest(TestCase):
    def setUp(self):
        self.sam = Member.objects.create(name='Sam', email='sam@gmail.com')
        self.steve = Member.objects.create(name='Steve', email='steve@gmail.com')
        self.stella = Member.objects.create(name='Stella', email='stella@gmail.com')
        
    def test_get_single_member(self):
        response = client.get(reverse('member_detail', kwargs={'pk': self.sam.pk}))
        member = Member.objects.get(pk=self.sam.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MemberSerializer(member)
        self.assertEqual(response.json(), serializer.data)

    def test_get_invalid_single_member(self):
        response = client.get(reverse('member_detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


##################################################################################
# test api/member/ POST
##################################################################################

class CreateNewMemberTest(TestCase):
    def setUp(self):
        self.valid_mem = {
            'name': 'Greg',
            'email': 'greg@gmail.com'
        }
        self.invalid_mem = {
            'name': 'Jill'
        }
    
    def test_create_valid_member(self):
        response = client.post(
            reverse('member_list'),
            data=json.dumps(self.valid_mem),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        member = Member.objects.get(name='Greg')
        self.assertEqual(member.name, 'Greg')
    
    def test_create_invalid_member(self):
        response = client.post(
            reverse('member_list'),
            data=json.dumps(self.invalid_mem),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


##################################################################################
# Test api/member/<id> PUT
##################################################################################

class UpdateSingleMemberTest(TestCase):
    def setUp(self):
        self.sam = Member.objects.create(name='Sam', email='sam@gmail.com')
        self.steve = Member.objects.create(name='Steve', email='steve@gmail.com')
        self.stella = Member.objects.create(name='Stella', email='stella@gmail.com')

        self.valid_mem = {
            'email': 'sammy@gmail.com'
        }

    def test_valid_update_member(self):
        response = client.put(
            reverse('member_detail', kwargs={'pk': self.sam.pk}),
            data=json.dumps(self.valid_mem),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        member = Member.objects.get(pk=self.sam.pk)
        self.assertEqual(member.name, 'Sam')
        self.assertEqual(member.email, 'sammy@gmail.com')
        serializer = MemberSerializer(member)
        self.assertEqual(response.json(), serializer.data)

##################################################################################   
# Test api/member/<id> DELETE
##################################################################################

class DeleteSingleMemberTest(TestCase):
    def setUp(self):
        self.sam = Member.objects.create(name='Sam', email='sam@gmail.com')
        self.steve = Member.objects.create(name='Steve', email='steve@gmail.com')
        self.stella = Member.objects.create(name='Stella', email='stella@gmail.com')
        
    def test_delete_single_member(self):
        response = client.delete(reverse('member_detail', kwargs={'pk': self.sam.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count = Member.objects.all().count()
        self.assertEqual(count, 2)

    def test_delete_invalid_single_member(self):
        response = client.delete(reverse('member_detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

##################################################################################   
# Test api/member/ DELETE
##################################################################################

class DeleteMembersTest(TestCase):
    def setUp(self):
        self.sam = Member.objects.create(name='Sam', email='sam@gmail.com')
        self.steve = Member.objects.create(name='Steve', email='steve@gmail.com')
        self.stella = Member.objects.create(name='Stella', email='stella@gmail.com')
        
    def test_delete_members(self):
        response = client.delete(reverse('member_list'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count = Member.objects.all().count()
        self.assertEqual(count, 0)

    
##################################################################################
# test api/book/ GET
##################################################################################

class GetAllBooksTest(TestCase):
    def setUp(self):
        Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

        
    def test_get_all_books(self):
        response = client.get(reverse('book_list'))
        books = Book.objects.all()
        count=books.count()
        self.assertEqual(count, 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.json(), serializer.data)

    
##################################################################################
# test api/book/<id> GET
##################################################################################

class GetSingleBookTest(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        self.book2 = Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        self.book3 = Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

       
    def test_get_single_book(self):
        response = client.get(reverse('book_detail', kwargs={'pk': self.book1.pk}))
        book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BookSerializer(book)
        self.assertEqual(response.json(), serializer.data)

    def test_get_invalid_single_book(self):
        response = client.get(reverse('book_detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

##################################################################################
# test api/book/ POST
##################################################################################

class CreateNewBookTest(TestCase):
    def setUp(self):
        self.valid_book = {
            'title': 'Leaving Time',
            'author': 'Jodi Picoult',
            'genre': 'ROM'
        }
        self.invalid_book = {
            'title': 'Small Great Things'
        }
    
    def test_create_valid_book(self):
        response = client.post(
            reverse('book_list'),
            data=json.dumps(self.valid_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(title='Leaving Time')
        self.assertEqual(book.title, 'Leaving Time')
    
    def test_create_invalid_book(self):
        response = client.post(
            reverse('book_list'),
            data=json.dumps(self.invalid_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


##################################################################################
# Test api/book/<id> PUT
##################################################################################

class UpdateSingleBookTest(TestCase):
    def setUp(self):

        self.book1 = Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        self.book2 = Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        self.book3 = Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

        self.valid_book = {
            'author': 'Jada Jones'
        }

    def test_valid_update_book(self):
        response = client.put(
            reverse('book_detail', kwargs={'pk': self.book2.pk}),
            data=json.dumps(self.valid_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book = Book.objects.get(pk=self.book2.pk)
        self.assertEqual(book.title, 'Small Great Things')
        self.assertEqual(book.author, 'Jada Jones')
        serializer = BookSerializer(book)
        self.assertEqual(response.json(), serializer.data)


##################################################################################   
# Test api/book/<id> DELETE
##################################################################################

class DeleteSingleBookTest(TestCase):
    def setUp(self):

        self.book1 = Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        self.book2 = Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        self.book3 = Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

    
    def test_delete_single_book(self):
        response = client.delete(reverse('book_detail', kwargs={'pk': self.book3.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count = Book.objects.all().count()
        self.assertEqual(count, 2)

    def test_delete_invalid_single_book(self):
        response = client.delete(reverse('book_detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

##################################################################################   
# Test api/book/ DELETE
##################################################################################

class DeleteBooksTest(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        self.book2 = Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        self.book3 = Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

        
    def test_delete_books(self):
        response = client.delete(reverse('book_list'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count = Book.objects.all().count()
        self.assertEqual(count, 0)



##################################################################################
# test api/recommendation/ GET
##################################################################################

class GetAllRecommendationTest(TestCase):
    def setUp(self):
        
        self.sam = Member.objects.create(name='Sam', email='sam@gmail.com')
        self.steve = Member.objects.create(name='Steve', email='steve@gmail.com')
        self.stella = Member.objects.create(name='Stella', email='stella@gmail.com')

        self.book1 = Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        self.book2 = Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        self.book3 = Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

        self.rec1 = Recommendation.objects.create(book=self.book1, member=self.sam)
        self.rec2 = Recommendation.objects.create(book=self.book1, member=self.steve)
        self.rec3 = Recommendation.objects.create(book=self.book2, member=self.stella)

        
    def test_get_all_recommendations(self):
        response = client.get(reverse('recommendation_list'))
        recommendations = Recommendation.objects.all()
        count=recommendations.count()
        self.assertEqual(count, 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = RecommendationViewSerializer(recommendations, many=True)
        self.assertEqual(response.json(), serializer.data)


##################################################################################
# test api/recommendation/ POST
##################################################################################

class CreateNewMemberTest(TestCase):
    def setUp(self):

        self.sam = Member.objects.create(name='Sam', email='sam@gmail.com')
        self.steve = Member.objects.create(name='Steve', email='steve@gmail.com')
        self.stella = Member.objects.create(name='Stella', email='stella@gmail.com')

        self.book1 = Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        self.book2 = Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        self.book3 = Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

        self.valid_rec = {
            'book': self.book1.id,
            'member': self.sam.id
        }
        self.invalid_rec = {
            'book': self.book1.id
        }
    
    def test_create_valid_recommendation(self):
        response = client.post(
            reverse('recommendation_list'),
            data=json.dumps(self.valid_rec),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recommendation = Recommendation.objects.get(member__name='Sam')
        self.assertEqual(recommendation.book, self.book1)
    
    def test_create_invalid_recommendation(self):
        response = client.post(
            reverse('recommendation_list'),
            data=json.dumps(self.invalid_rec),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


##################################################################################   
# Test api/recommendation/ DELETE
##################################################################################

class DeleteRecommendationsTest(TestCase):
    def setUp(self):
        
        self.sam = Member.objects.create(name='Sam', email='sam@gmail.com')
        self.steve = Member.objects.create(name='Steve', email='steve@gmail.com')
        self.stella = Member.objects.create(name='Stella', email='stella@gmail.com')

        self.book1 = Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        self.book2 = Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        self.book3 = Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

        self.rec1 = Recommendation.objects.create(book=self.book1, member=self.sam)
        self.rec2 = Recommendation.objects.create(book=self.book1, member=self.steve)
        self.rec3 = Recommendation.objects.create(book=self.book2, member=self.stella)

        
    def test_delete_recommendation(self):
        response = client.delete(reverse('recommendation_list'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count = Recommendation.objects.all().count()
        self.assertEqual(count, 0)


##################################################################################   
# Test api/recommendation/<id> DELETE
##################################################################################

class DeleteSingleRecommendationTest(TestCase):
    def setUp(self):

        self.sam = Member.objects.create(name='Sam', email='sam@gmail.com')
        self.steve = Member.objects.create(name='Steve', email='steve@gmail.com')
        self.stella = Member.objects.create(name='Stella', email='stella@gmail.com')

        self.book1 = Book.objects.create(title='Wish You Were Here', author='Jodi Picoult', genre='ROM')
        self.book2 = Book.objects.create(title='Small Great Things', author='Jodi Picoult', genre='ROM')
        self.book3 = Book.objects.create(title='Leaving Time', author='Jodi Picoult', genre='ROM')

        self.rec1 = Recommendation.objects.create(book=self.book1, member=self.sam)
        self.rec2 = Recommendation.objects.create(book=self.book1, member=self.steve)
        self.rec3 = Recommendation.objects.create(book=self.book2, member=self.stella)

    
    def test_delete_single_recommendation(self):
        response = client.delete(reverse('recommendation_detail', kwargs={'pk': self.rec1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count = Recommendation.objects.all().count()
        self.assertEqual(count, 2)

    def test_delete_invalid_single_recommendation(self):
        response = client.delete(reverse('recommendation_detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
