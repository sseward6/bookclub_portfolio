from django.shortcuts import render
from django.db.models import Max
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
#from django.http import HttpResponse
#from django.http import HttpRequest 

from bookclub.models import Book, Member, Recommendation
from bookclub.serializers import BookSerializer, MemberSerializer, RecommendationSerializer, RecommendationViewSerializer
from rest_framework.decorators import api_view

# Create your views here.

#def index(request):
#    print("------------------------- I AM HERE")
#    queryset = Tutorial.objects.all()
#    return render(request, "tutorials/index.html", {'tutorials': queryset})


"""
class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'bookclub/index.html'

    def get(self, request):
        queryset = Book.objects.all()
        return Response({'book': queryset})
"""


#  just return a message for homepage.  

@api_view()
def index(request):
    return JsonResponse({'message': 'Welcome to nc_bookclub!'}, status=status.HTTP_200_OK)
    
    
############################################################################################
#                              BOOK VIEWS
############################################################################################

@api_view(['GET', 'POST', 'DELETE'])
def book_list(request):
    # get all books - if json body then use to filter results
    if request.method == 'GET':
        books = Book.objects.all()
        
        title=author=genre=None
    
        if request.data:
            print(f"request.data exists:  {request.data}")
            if "title" in request.data:
                title=request.data['title']
            if "author" in request.data:
                author=request.data['author']
            if "genre" in request.data:
                genre=request.data['genre']
            
        if title is not None:
            books = books.filter(title__icontains=title)
        
        if author is not None:
            books = books.filter(author__icontains=author)
        
        if genre is not None:
            books = books.filter(genre__iexact=genre)

        books_serializer = BookSerializer(books, many=True)
        return JsonResponse(books_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        # add new Book
        book_data = JSONParser().parse(request)
        book_serializer = BookSerializer(data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return JsonResponse(book_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(book_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # delete all Books
        count = Book.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Books were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)

# BOOK DETAIL BY PRIMARY KEY

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return JsonResponse({'message': 'The book does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        book_serializer = BookSerializer(book)
        return JsonResponse(book_serializer.data)

    elif request.method == 'PUT':
        # update book
        book_data = JSONParser().parse(request)
        book_serializer = BookSerializer(book, data=book_data, partial=True)
        if book_serializer.is_valid():
            book_serializer.save()
            return JsonResponse(book_serializer.data)
        return JsonResponse(book_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # delete single book
        book.delete()
        return JsonResponse({'message': 'Book was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)

############################################################################################
#                              MEMBER VIEWS
############################################################################################


@api_view(['GET', 'POST', 'DELETE'])
def member_list(request):
    if request.method == 'GET':
        # Get all members -- if json data exists use to filter

        members = Member.objects.all()
        name=email=None
       
        if request.data:
            if "name" in request.data:
                name=request.data['name']
            if "email" in request.data:
                email=request.data['email']
    
        if name is not None:
            members = members.filter(name__icontains=name)
        
        if email is not None:
            members = members.filter(email__icontains=email)
    
        members_serializer = MemberSerializer(members, many=True)
        return JsonResponse(members_serializer.data, safe=False)
     

    elif request.method == 'POST':
        # add new member
        member_data = JSONParser().parse(request)
        member_serializer = MemberSerializer(data=member_data)

        if member_serializer.is_valid():
            member_serializer.save()
            return JsonResponse(member_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(member_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # delete all members
        count = Member.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Members were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)

# MEMBER DETAILS USING PRIMARY KEY

@api_view(['GET', 'PUT', 'DELETE'])
def member_detail(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return JsonResponse({'message': 'The member does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        member_serializer = MemberSerializer(member)
        return JsonResponse(member_serializer.data)

    elif request.method == 'PUT':
        # update member
        member_data = JSONParser().parse(request)
        member_serializer = MemberSerializer(member, data=member_data, partial=True)
        if member_serializer.is_valid():
            member_serializer.save()
            return JsonResponse(member_serializer.data)
        return JsonResponse(member_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # delete single member
        member.delete()
        return JsonResponse({'message': 'Member was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)



############################################################################################
#                              RECOMMENDATION VIEWS
############################################################################################


@api_view(['GET', 'POST', 'DELETE'])
def recommendation_list(request):

    if request.method == 'GET':

        # get all recommendations - if json data, use to filter
        recommendations = Recommendation.objects.all().order_by('-r_date')
        
        name=title=author=genre=r_date=None
        if request.data:
            print(f"request.data exists:  {request.data}")
            if "name" in request.data:
                name=request.data['name']
            if "title" in request.data:
                title=request.data['title']
            if "author" in request.data:
                author=request.data['author']
            if "genre" in request.data:
                genre=request.data['genre']
            if "r_date" in request.data:
                r_date=request.data['r_date']
            
        if name is not None:
            recommendations = recommendations.filter(member__name__icontains=name)
        if title is not None:
            recommendations = recommendations.filter(book__title__icontains=title)
        if author is not None:
            recommendations = recommendations.filter(book__author__icontains=author)
        if genre is not None:
            recommendations = recommendations.filter(book__genre__iexact=genre)
        if r_date is not None:
            recommendations = recommendations.filter(r_date__contains=r_date)

        recs_serializer = RecommendationViewSerializer(recommendations, many=True)
        return JsonResponse(recs_serializer.data, safe=False)    

    elif request.method == 'POST':
        # add a recommendation
        rec_data = JSONParser().parse(request)
        rec_serializer = RecommendationSerializer(data=rec_data)
        if rec_serializer.is_valid():
            rec_serializer.save()
            return JsonResponse(rec_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(rec_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # delete all recommendations
        count = Recommendation.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Recommendations were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


# RECOMMENDATION DETAILS USING PRIMARY KEY

@api_view(['DELETE'])
def recommendation_detail(request, pk):

    try:
        recommendation = Recommendation.objects.get(pk=pk)
    except Recommendation.DoesNotExist:
        return JsonResponse({'message': 'The recommendation does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        # delete a single recommendation
        recommendation.delete()
        return JsonResponse({'message': 'Member was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
                            

# LATEST RECOMMENDATIONS FOR EACH GENRE

@api_view(['GET'])
def recommendation_latest(request):
    
    if request.method == 'GET':
        recommendations = Recommendation.objects.values('book__genre').annotate(latest_date=Max('r_date'))
        books = Book.objects.all()
        
        result = Book.objects.none()
        for r in recommendations:
            rec_books = books.filter(genre__iexact=r['book__genre'], recommendation__r_date__contains=r['latest_date']).distinct()
            result = result.union(rec_books)

        result=result.order_by('genre') 
        books_serializer = BookSerializer(result, many=True)
        return JsonResponse(books_serializer.data, safe=False)