from django.urls import path
from bookclub import views as bookclub_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('', bookclub_views.index, name='home'),
    #path('', bookclub_views.index.as_view(), name='home'),
    path('', bookclub_views.index),
    path('api/book/', bookclub_views.book_list),
    path('api/book/<int:pk>/', bookclub_views.book_detail),
    path('api/member/', bookclub_views.member_list),
    path('api/member/<int:pk>/', bookclub_views.member_detail),
    path('api/recommendation/', bookclub_views.recommendation_list)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)