import re
import json
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class GoodreadsScraper:
    def __init__(self, keyword, first_page, last_page):
        self.base_url = "https://www.goodreads.com/search"
        self.default_params = {
            "query": keyword,
            "search_type": "books",
            "tab": "books",
            "utf8": "✓"
        }
        
        self.first_page = first_page
        self.last_page = last_page
        self.urls = []
        self.scraped_books = []

    def scrape_books(self):
        for page_num in range(int(self.first_page), int(self.last_page) + 1):
            params = self.default_params.copy()
            params["page"] = page_num
            response = requests.get(self.base_url, params=params)
            print(f"Scraping page {page_num} --> {response.url}")

            if response.status_code == 200:
                print("\033[92mRequest successful\033[0m")
                soup = BeautifulSoup(response.text, "html.parser")
                table = soup.find("table", class_="tableList")

                if table:
                    rows = table.find_all("tr")
                    for row in rows:
                        book_info = self.extract_book_info(row)
                        self.scraped_books.append(book_info)
                    
                    print("\033[94m" + f"\nFetching details for books..." + "\033[0m")
                    books_details = self.get_book_details(self.urls)

                    if self.scraped_books:
                        for i in range(len(self.scraped_books)):
                            if self.scraped_books[i] and books_details[i]:
                                self.scraped_books[i].update(books_details[i])
                            print(f"\033[95mBook {i + 1}\033[0m")
                            for info in self.scraped_books[i]:
                                print(f"{info}: {self.scraped_books[i][info]}")
                            print("\033[93m" + '-'*125 + "\033[0m")
                else:
                    print(f"No table found on page {page_num}.")
            else:
                print(f"\033[91mFailed to fetch page {page_num}. Status code: {response.status_code}\033[0m")
            
            time.sleep(5)
            
        return self.scraped_books

    def extract_book_info(self, row):
        title = row.find("span", itemprop="name")
        title = title.text.strip() if title else 'N/A'

        authors = row.find_all("div", class_="authorName__container")
        people = [author.text.strip().replace(',', '') for author in authors] if authors else 'N/A'

        minirating_span = row.find("span", class_="minirating")
        if minirating_span:
            rating_text = minirating_span.text.strip()
            
            avg_rating_match = re.search(r'([\d.]+)\s+avg rating', rating_text)
            if avg_rating_match:
                avg_rating = avg_rating_match.group(1)
            else:
                avg_rating = None
            
            num_ratings_match = re.search(r'(\d+(?:,\d+)*)\s+ratings', rating_text)
            if num_ratings_match:
                num_ratings = num_ratings_match.group(1)
            else:
                num_ratings = None
        
        else:
            avg_rating = None
            num_ratings = None

        published = row.find('span', class_='greyText smallText uitext')
        span_text = published.get_text(strip=True) if published else 'N/A'
        pattern = r'published\s*(\d+)'
        match = re.search(pattern, span_text)
        published_year = match.group(1) if match else None

        edition = row.find('a', class_='greyText')
        editions = edition.text.strip().split()[0] if edition else None

        book_info = {
            "title": title,
            "author(s)": ", ".join(people),
            "avg_rating": avg_rating,
            "num_ratings": num_ratings,
            "published_year": published_year,
            "editions": editions
        }

        href = row.find('a', class_='bookTitle')['href']
        url = "https://www.goodreads.com" + href
        self.urls.append(url)

        return book_info

    def get_book_details(self, urls):
        def fetch_detail(url):
            response = requests.get(url)
            book_info = {}

            if response.status_code == 200:
                print(f"    {url}")
                print("    \033[92mRequest successful\033[0m\n")

                soup = BeautifulSoup(response.content, "html.parser")

                reviews_count_tag = soup.find("span", {"data-testid": "reviewsCount"})
                book_info['reviews_count'] = reviews_count_tag.text.strip().split()[0] if reviews_count_tag else "N/A"

                image_tag = soup.find("img", {"class": "ResponsiveImage"})
                book_info['image_url'] = image_tag["src"] if image_tag else "N/A"

                kindle_price_tag = soup.find("button", {"class": "Button--buy"})
                book_info['kindle_price'] = kindle_price_tag.text.strip() if kindle_price_tag else "N/A"

                book_data_script = soup.find("script", {"type": "application/ld+json"})
                if book_data_script:
                    book_data = json.loads(book_data_script.string)
                    book_info['book_format'] = book_data.get('bookFormat', 'N/A')
                    book_info['number_of_pages'] = book_data.get('numberOfPages', None)
                    book_info['language'] = book_data.get('inLanguage', 'N/A')
                    book_info['isbn'] = book_data.get('isbn', 'N/A')
                    book_info['award(s)'] = book_data.get('awards', 'N/A')
                else:
                    book_info['book_format'] = 'N/A'
                    book_info['number_of_pages'] = None
                    book_info['language'] = 'N/A'
                    book_info['isbn'] = 'N/A'
                    book_info['award(s)'] = 'N/A'
                
                return book_info
            
            else:
                print(f"\033[91mFailed to fetch page. Status code: {response.status_code}\033[0m")
                return None

        with ThreadPoolExecutor() as executor:
            books_info = list(executor.map(fetch_detail, urls))
        
        return books_info
