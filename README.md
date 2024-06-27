# Goodreads Django Project

This Django project is designed to scrape book data from Goodreads and store it in a local database. It consists of a Django app named `book_scraper` which handles the scraping functionality and provides a user interface for searching and viewing books.

## Setup

1. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

2. Run the development server:

    ```
    python manage.py runserver
    ```

## Usage

### Scraping Books

To scrape books from Goodreads and store them in the database, you can use the `scrapebooks` management command. This command takes two arguments:

- `keyword`: The keyword to search on Goodreads
- `first_page`: First page to scrape
- `last_page`: Last page to scrape

Example usage:

```
python manage.py scrapebooks <keyword> <first_page> <last_page>
```

### Searching and Viewing Books

1. Navigate to the home page (`/`) to access the search form.
2. Enter a keyword and range of pages to scrape, then submit the form.
3. After scraping, you will be redirected to the book list page (`/book-list/`) where you can view the scraped books.
4. Click on a book title to view its details.

## Project Structure

- `goodreads/`: Django project directory.
  - `book_scraper/`: Django app directory.
    - `management/`: Contains management commands.
      - `commands/`: Contains custom management commands.
        - `scrapebooks.py`: Management command to scrape books from Goodreads.
    - `migrations/`: Database migrations.
    - `templates/`: HTML templates.
    - `models.py`: Defines the database models.
    - `forms.py`: Defines Django forms.
    - `scraping.py`: Contains the GoodreadsScraper class for scraping book data.
    - `urls.py`: URL configurations for the app.
    - `views.py`: Contains view functions.
