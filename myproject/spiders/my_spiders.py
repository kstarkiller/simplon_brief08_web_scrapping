import scrapy
from pymongo import MongoClient
import os

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://books.toscrape.com/catalogue/page-1.html']

    def parse(self, response):
        # Extracting data from each book on the current page
        for book in response.css('li.col-xs-6.col-sm-4.col-md-3.col-lg-3'):
            rating_class = book.css('p.star-rating::attr(class)').get()
            rating = rating_class.split()[1] if rating_class else None
            
            image_url = book.css('div.image_container a img::attr(src)').get()
            image_name = os.path.basename(image_url) if image_url else None

            book_data = {
                'title': book.css('h3 a::attr(title)').get(),
                'image_names': [image_name],
                'rating': rating,
                'price': book.css('p.price_color::text').get(),
            }

            detail_page_url = response.urljoin(book.css('h3 a::attr(href)').get())
            request = scrapy.Request(detail_page_url, callback=self.parse_book_details)
            request.meta['book_data'] = book_data 
            yield request

        # Handling pagination
        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_book_details(self, response):
        book_data = response.meta['book_data'] 

        category = response.css('ul.breadcrumb li:nth-last-child(2) a::text').get()
        book_data['category'] = category

        description = response.css('article.product_page p:not([class])::text').get()
        book_data['description'] = description

        # Appel de la fonction pour stocker dans MongoDB
        self.store_in_mongodb(book_data)

        yield book_data

    def store_in_mongodb(self, book_data):
        # Connexion à la base de données MongoDB
        client = MongoClient('mongodb://127.0.0.1:27017/')
        db = client['biblio']
        collection = db['books']

        # Insérer les données dans la collection
        collection.insert_one(book_data)

        # Afficher les résultats
        self.log(f"Storing in MongoDB - {book_data['title']}")

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    # Créer un processus de crawling
    process = CrawlerProcess()

    # Ajouter le spider au processus
    process.crawl(MySpider)

    # Lancer le processus de crawling
    process.start()
