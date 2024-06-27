from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_books, name='search_books'),
    path('book-list/', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'), 
]
