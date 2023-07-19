import scrapy

class BatmanSpider(scrapy.Spider):
    name = "batman"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            yield{
                'name': book.css('h3 a::text').get(),
                'url': book.css('h3 a').attrib['href'],
                'price': book.css('div p::text').get(),
                'rating': book.css('p').attrib['class']

            }

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_rul = 'https://books.toscrape.com/' + next_page
            else:
                next_page_rul = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_rul, callback=self.parse)
