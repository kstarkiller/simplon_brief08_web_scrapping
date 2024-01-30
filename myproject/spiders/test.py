import scrapy
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        # Récupérer les liens vers les catégories
        category_links = response.css('ul.nav-list > li > ul > li > a::attr(href)').extract()

        # Pour chaque catégorie, suivre le lien et extraire les titres des livres
        for category_link in category_links:
            yield scrapy.Request(url=response.urljoin(category_link), callback=self.parse_category)

    def parse_category(self, response):
        # Récupérer le nom de la catégorie
        category_name = response.css('h1::text').extract_first().strip()

        # Récupérer les titres des livres dans la catégorie
        book_titles = response.css('h3 > a::attr(title)').extract()

        # Stocker les résultats dans MongoDB
        self.store_in_mongodb(category_name, book_titles)

    def store_in_mongodb(self, category_name, book_titles):
        # Connexion à la base de données MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['biblio']
        collection = db['books']

        # Préparer les données à insérer dans la base de données
        data = {
            'category_name': category_name,
            'book_titles': book_titles,
        }

        # Insérer les données dans la collection
        collection.insert_one(data)

        # Afficher les résultats
        self.log(f"Storing in MongoDB - {category_name}: {book_titles}")