# import scrapy

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     allowed_domains = ["quotes.toscrape.com"]
#     start_urls = ["https://quotes.toscrape.com"]

#     def parse(self, response):
#         pass


import scrapy
from scrapy import item
from scrapytutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            item = QuoteItem()
            item['text'] = quote.css("span.text::text").get()
            item['author'] = quote.css("small.author::text").get()
            item['tags'] = quote.css("div.tags a.tag::text").getall()
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

            