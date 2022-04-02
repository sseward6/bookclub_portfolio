from rest_framework import serializers
from bookclub.models import Book, Member, Recommendation


# BOOK SERIALIZER
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre')


# MEMBER SERIALIZER
class MemberSerializer(serializers.ModelSerializer): 
    books = BookSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Member
        fields = ('id', 'name', 'email', 'books')
        extra_kwargs = {"book" : {"required" : False, "allow_null" : True}}

# RECOMMENDATION SERIALIZER FOR POST
class RecommendationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recommendation
        fields = ('id', 'member', 'book', 'r_date')
  
        
# RECOMMENDATION SERIALIZER FOR GET
class RecommendationViewSerializer(serializers.ModelSerializer):
    
    member_name = serializers.ReadOnlyField(source = 'member.name')
    book_title = serializers.ReadOnlyField(source = 'book.title')
    book_author = serializers.ReadOnlyField(source = 'book.author')
    book_genre = serializers.ReadOnlyField(source = 'book.genre')
    
    class Meta:
        model = Recommendation
        fields = ('id', 'member_name', 'book_title', 'book_author', 'book_genre', 'r_date')