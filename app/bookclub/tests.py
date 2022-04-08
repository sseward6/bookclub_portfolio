from django.test import TestCase, Client
from django.urls import reverse
from bookclub.models import Book, Member, Recommendation
import pytest

# Create your tests here.
client = Client()

# test url

def test_homepage_access():
    url = reverse('home')
    assert url == "/"

def test_book_list_access():
    url = reverse('book_list')
    assert url == "/api/book/"

def test_member_list_access():
    url = reverse('member_list')
    assert url == "/api/member/"

def test_recommendation_list_access():
    url = reverse('recommendation_list')
    assert url == "/api/recommendation/"

def test_recommendation_latest_access():
    url = reverse('recommendation_latest')
    assert url == "/api/recommendation/latest/"


# Test model

class MemberTest(TestCase):
    def setUp(self):
        Member.objects.create(name='Joe', email='joe@gmail.com')

    def test_member_name(self):
        member_joe = Member.objects.get(name='Joe')
        self.assertEqual(member_joe.name, "Joe")

# test book model

@pytest.fixture
def new_book(db):
    book = Book.objects.create(
        title='Oathbringer',
        author='Brandon Sanderson',
        genre='SCF'
    )
    return book

def test_search_book(new_book):
    assert Book.objects.filter(title='Oathbringer').exists()

def test_update_book(new_book):
    new_book.title = 'Oathtaker'
    new_book.save()
    assert Book.objects.filter(title='Oathtaker').exists()

# test member model

@pytest.fixture
def new_member(db):
    member = Member.objects.create(
        name ='Judy',
        email='judy@gmail.com'
    )
    return member


def test_search_member(new_member):
    assert Member.objects.filter(name ='Judy').exists()

def test_update_member(new_member):
    new_member.email = 'judy@hotmail.com'
    new_member.save()
    assert Member.objects.filter(email='judy@hotmail.com').exists()

# test recommendation model

@pytest.fixture
def new_recommendation(db, new_book, new_member):
    recommendation = Recommendation.objects.create(
        book = new_book,
        member = new_member
    )
    return recommendation

def test_search_reccomendation(new_recommendation):
    assert Recommendation.objects.filter(book__title='Oathbringer', member__name='Judy').exists()


