from functools import partial
from django.shortcuts import render
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
# def index(request):
#     return render(request, "tutorials/index.html")


#def index(request):
#    print("------------------------- I AM HERE")
#    queryset = Tutorial.objects.all()
#    return render(request, "tutorials/index.html", {'tutorials': queryset})

"""
def index(request):
        return JsonResponse(
            {
                'message': 'Welcome to the Book Club App!'
            },
            status=status.HTTP_204_NO_CONTENT)
"""
"""
class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'bookclub/index.html'

    def get(self, request):
        queryset = Book.objects.all()
        return Response({'book': queryset})
"""



@api_view()
def index(request):
    return JsonResponse({'message': 'Welcome to nc_bookclub!'}, status=status.HTTP_200_OK)
    
    
############################################################################################
#                              BOOK VIEWS
############################################################################################

@api_view(['GET', 'POST', 'DELETE'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        print("********************************************************************got all books")
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
            print(f"*******************************************************************title not None -- filter")
            books = books.filter(title__icontains=title)
        
        
        if author is not None:
            print(f"*******************************************************************author not None -- filter")
            books = books.filter(author__icontains=author)
    
        
        if genre is not None:
            print(f"*******************************************************************genre not None -- filter")
            books = books.filter(genre__iexact=genre)

        books_serializer = BookSerializer(books, many=True)
        return JsonResponse(books_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        book_data = JSONParser().parse(request)
        book_serializer = BookSerializer(data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return JsonResponse(book_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(book_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
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
        book_data = JSONParser().parse(request)
        book_serializer = BookSerializer(book, data=book_data, partial=True)
        if book_serializer.is_valid():
            book_serializer.save()
            return JsonResponse(book_serializer.data)
        return JsonResponse(book_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({'message': 'Book was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)

############################################################################################
#                              MEMBER VIEWS
############################################################################################


@api_view(['GET', 'POST', 'DELETE'])
def member_list(request):
    if request.method == 'GET':
        members = Member.objects.all()
        print("********************************************************************got all Members")

        name=email=None
        # request.GET is empty so getting any input filters from request.data
        if request.data:
            print(f"request.data exists:  {request.data}")
            if "name" in request.data:
                name=request.data['name']
            if "email" in request.data:
                email=request.data['email']
            
        else:
            print("Null request data")

    
        if name is not None:
            print(f"*******************************************************************name not None -- filter")
            members = members.filter(name__icontains=name)
        
    
        if email is not None:
            print(f"*******************************************************************email not None -- filter")
            members = members.filter(email__icontains=email)
    
       
        members_serializer = MemberSerializer(members, many=True)
        return JsonResponse(members_serializer.data, safe=False)
     

    elif request.method == 'POST':
        print("member post")
        member_data = JSONParser().parse(request)
        print(f"data is:  {member_data}")
        #member_serializer = MemberSerializer(data=member_data, partial=True)
        member_serializer = MemberSerializer(data=member_data)

        if member_serializer.is_valid():
            member_serializer.save()
            return JsonResponse(member_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(member_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
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
        member_data = JSONParser().parse(request)
        member_serializer = MemberSerializer(member, data=member_data, partial=True)
        if member_serializer.is_valid():
            member_serializer.save()
            return JsonResponse(member_serializer.data)
        return JsonResponse(member_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        member.delete()
        return JsonResponse({'message': 'Member was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)



############################################################################################
#                              RECOMMENDATION VIEWS
############################################################################################


@api_view(['GET', 'POST', 'DELETE'])
def recommendation_list(request):

    print("Got to recommendation_list view")
    if request.method == 'GET':
        recommendations = Recommendation.objects.all().order_by('-r_date')
        print("********************************************************************got all Recommendations")
        
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
        rec_data = JSONParser().parse(request)
        rec_serializer = RecommendationSerializer(data=rec_data)
        if rec_serializer.is_valid():
            rec_serializer.save()
            return JsonResponse(rec_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(rec_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Recommendation.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Recommendations were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)



#############################################################################################
"""
@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Tutorial.objects.filter(published=True)

    if request.method == 'GET':
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
"""