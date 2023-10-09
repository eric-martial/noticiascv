from ..items import ArticleItem
import scrapy
import dateparser
from datetime import datetime


class anacao(scrapy.Spider):
    name = "anacao"
    allowed_domains = ['anacao.cv']
    base_url = 'https://anacao.cv'
    start_urls = [
        'https://santiagomagazine.cv/economia',
        'https://santiagomagazine.cv/politica',
        'https://santiagomagazine.cv/cultura',
        'https://santiagomagazine.cv/diaspora',
        'https://santiagomagazine.cv/editorial',
        'https://santiagomagazine.cv/outros-mundos',
        'https://santiagomagazine.cv/sociedad'
    ]

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        hero_urls = response.css('div#feat-top-wrap a::attr(href)').getall()
        page_urls = hero_urls.append(response.css('div#archive-list-wrap li>a::attr(href)').getall())

        for page_url in page_urls:
            page_url = response.urljoin(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse_news)

        next_page = response.css('div.pagination a::attr(href)').getall()[-2]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    