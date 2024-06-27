from django.db import models

class Book(models.Model):
    keyword = models.TextField()
    title = models.CharField(max_length=255)
    authors = models.TextField()
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    num_ratings = models.CharField(max_length=20, null=True)
    published_year = models.IntegerField(null=True)
    editions = models.IntegerField(null=True)
    reviews_count = models.CharField(max_length=20, null=True)
    image_url = models.URLField(null=True)
    kindle_price = models.CharField(max_length=50, null=True)
    book_format = models.CharField(max_length=100, null=True)
    number_of_pages = models.IntegerField(null=True)
    language = models.CharField(max_length=50, null=True)
    isbn = models.CharField(max_length=20, null=True)
    awards = models.TextField(null=True)

    class Meta:
        unique_together = ('title', 'authors')

    def __str__(self):
        return self.title
