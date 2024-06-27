from book_scraper.models import Book
from django.core.management.base import BaseCommand, CommandError
from book_scraper.scraping import GoodreadsScraper


class Command(BaseCommand):
    help = 'Scrape books from Goodreads and store them in the database'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str, help='Keyword to search on Goodreads')
        parser.add_argument('first_page', type=int, help='First page to scrape')
        parser.add_argument('last_page', type=int, help='Last page to scrape')

    def handle(self, *args, **options):
        keyword = options['keyword']
        first_page = options['first_page']
        last_page = options['last_page']

        if not keyword or not first_page or not last_page:
            raise CommandError
        
        scraper = GoodreadsScraper(keyword, first_page, last_page)
        scraped_books = scraper.scrape_books()

        for book_info in scraped_books:
            self.save_book(book_info, keyword)

        self.stdout.write(self.style.SUCCESS('Successfully scraped and saved books.'))

    def save_book(self, book_info, keyword):

        book = Book(
            keyword=keyword.strip().lower(),
            title=book_info['title'],
            authors=book_info['author(s)'],
            avg_rating=book_info['avg_rating'],
            num_ratings=book_info['num_ratings'],
            published_year=book_info['published_year'],
            editions=book_info['editions'],
            reviews_count=book_info['reviews_count'],
            image_url=book_info['image_url'],
            kindle_price=book_info['kindle_price'],
            book_format=book_info['book_format'],
            number_of_pages=book_info['number_of_pages'],
            language=book_info['language'],
            isbn=book_info['isbn'],
            awards=book_info['award(s)']
        )
        if not Book.objects.filter(title=book_info['title'], authors=book_info['author(s)']).exists():
            book.save()
        