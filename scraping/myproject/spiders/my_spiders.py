import scrapy
import os
from pymongo import MongoClient
from io import BytesIO
from PIL import Image

# Importation pour MongoDBManager
from MongoDBOps import MongoDBManager

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://books.toscrape.com/catalogue/page-1.html']
    mongo_manager = MongoDBManager()

    def parse(self, response):
        # Extraction des données de chaque livre sur la page principale
        for book in response.css('li.col-xs-6.col-sm-4.col-md-3.col-lg-3'):
            rating_class = book.css('p.star-rating::attr(class)').get()
            rating = rating_class.split()[1] if rating_class else None
                
            image_url = book.css('div.image_container a img::attr(src)').get()
            image_name = image_url.split('/')[-1] if image_url else None

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

        # Gestion de la pagination
        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

        # Récupérer tous les liens de catégories
        category_links = response.css('html.no-js body#default.default div.container-fluid.page div.page_inner div.row aside.sidebar.col-sm-4.col-md-3 div.side_categories ul.nav.nav-list ul li a::attr(href)').extract()

        # Parcourir toutes les catégories
        for category_link in category_links:
            yield scrapy.Request(url=response.urljoin(category_link), callback=self.parse_category)

    def parse_category(self, response):
        # Traitement de chaque page de catégorie comme nécessaire
        # Ajoutez ici le code pour extraire les détails des livres de la catégorie

        # Gérer la pagination des catégories (si nécessaire)
        next_category_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_category_page:
            yield scrapy.Request(url=response.urljoin(next_category_page), callback=self.parse_category)

    def parse_book_details(self, response):
        # Extraction des détails du livre
        book_img_url = response.css('article.product_page img::attr(src)').get()
        title = response.css('h1::text').get()
        rating_class = response.css('p.star-rating::attr(class)').get()
        rating = rating_class.split()[1] if rating_class else None
        image_url = response.css('div.image_container a img::attr(src)').get()
        image_name = image_url.split('/')[-1] if image_url else None
        
        price = response.css('p.price_color::text').get()
        category = response.css('ul.breadcrumb li:nth-last-child(2) a::text').get()
        description = response.css('article.product_page p:not([class])::text').get()
        upc = response.css('article.product_page th:contains("UPC") + td::text').get()
        product_type = response.css('article.product_page th:contains("Product Type") + td::text').get()
        book_Price_excl_tax = response.css('article.product_page th:contains("Price (excl. tax)") + td::text').get()
        book_Price_incl_tax = response.css('article.product_page th:contains("Price (incl. tax)") + td::text').get()
        book_tax = response.css('article.product_page th:contains("Tax") + td::text').get()
        book_availability = response.css('article.product_page th:contains("Availability") + td::text').get()
        book_nb_of_review = response.css('article.product_page th:contains("Number of reviews") + td::text').get()

        # Télécharger l'image binaire
        request = scrapy.Request(url=response.urljoin(book_img_url), callback=self.save_image)
        request.meta['book_data'] = {
            'category': category,
            'book_img_url':book_img_url,
            'image_names': [image_name],
            'title': title,
            'rating': rating,
            'price': price,
            'availability': book_availability,
            'description': description,
            'upc': upc,
            'product_type': product_type,
            'price_excluding_tax': book_Price_excl_tax,
            'price_including_tax': book_Price_incl_tax,
            'tax': book_tax,
            'availability': book_availability,
            'number_of_reviews': book_nb_of_review
        }
        yield request

    def save_image(self, response):
        # Obtention du nom de fichier à partir de l'URL de l'image
        image_name = os.path.basename(response.url)

        # Sauvegarde de l'image binaire dans MongoDB avec les métadonnées du livre
        book_data = response.meta['book_data']
        image_binary = BytesIO(response.body)
        image_binary.seek(0)

        book_detail = {
            'category': book_data['category'],
            'book_img_url': book_data['book_img_url'],
            'image_names': book_data['image_names'],
            'title': book_data['title'],
            'rating': book_data['rating'],
            'price': book_data['price'],
            'availability': book_data['availability'],
            'description': book_data['description'],
            'upc': book_data['upc'],
            'product_type': book_data['product_type'],
            'price_excluding_tax': book_data['price_excluding_tax'],
            'price_including_tax': book_data['price_including_tax'],
            'tax': book_data['tax'],
            'number_of_reviews': book_data['number_of_reviews'],
            'image_binary': image_binary.read()
        }

        # Sauvegarde dans MongoDB
        self.mongo_manager.store_in_mongodb(book_detail)
        yield book_detail

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    # Créer un processus de crawling
    process = CrawlerProcess()

    # Ajouter la spider au processus
    process.crawl(MySpider)

    # Lancer le processus de crawling
    process.start()


