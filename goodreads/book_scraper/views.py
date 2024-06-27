from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Book
from .forms import SearchForm
from django.core.management import call_command


def search_books(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            first_page = form.cleaned_data['first_page']
            last_page = form.cleaned_data['last_page']
            call_command('scrapebooks', [keyword, first_page, last_page])
            return redirect('book_list')
    else:
        form = SearchForm()
    return render(request, 'book_scraper/search.html', {'form': form})


def book_list(request):
    book_list = Book.objects.all().order_by('-id')
    for book in book_list:
        book.shortened_title = shorten_title(book.title)
    paginator = Paginator(book_list, 10)  # Display 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book_scraper/book_list.html', {'page_obj': page_obj})


def shorten_title(title):
    words = title.split()
    if len(words) <= 5:
        return ' '.join(words)
    else:
        return ' '.join(words[:5]) + '...'


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'book_scraper/book_detail.html', {'book': book})
