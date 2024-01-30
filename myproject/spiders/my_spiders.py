import scrapy
import os

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://books.toscrape.com/catalogue/page-1.html']

    def parse(self, response):
        # Extracting data from each book on the current page
        for book in response.css('li.col-xs-6.col-sm-4.col-md-3.col-lg-3'):
            # Capture the class attribute of the rating element
            rating_class = book.css('p.star-rating::attr(class)').get()
            # Split the class attribute by spaces and get the second item which should be the rating word
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

        # Extracting category
        category = response.css('ul.breadcrumb li:nth-last-child(2) a::text').get()
        book_data['category'] = category

        # Extracting description
        description = response.css('article.product_page p:not([class])::text').get()
        book_data['description'] = description

        yield book_data