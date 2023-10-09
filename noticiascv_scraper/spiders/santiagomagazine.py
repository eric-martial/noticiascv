from ..items import ArticleItem
import scrapy
import dateparser
from datetime import datetime


class SantiagoMagaZineSpider(scrapy.Spider):
    name = "santiagomagazine"
    allowed_domains = ['santiagomagazine.cv']
    base_url = 'https://santiagomagazine.cv'
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
        page_urls = response.css('h3.title-semibold-dark a::attr(href)').getall()

        self.logger.info(page_urls)

        for page_url in page_urls:
            page_url = response.urljoin(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse_news)

        next_page = response.css('div.pagination-btn-wrapper li.page-item a::attr(href)').extract()[-1]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def __normalize_date(self, date_obj):
        if not isinstance(date_obj, datetime):
            return None
        return date_obj.strftime('%Y-%m-%d')

    def parse_news(self, response):
        req_url = response.url

        self.logger.info(f"request page: {req_url}")

        item = ArticleItem()
        item['source'] = self.name
        article_block = response.css('div.news-details-layout1')
        item['title'] = article_block.css('h2.title-semibold-dark::text').get()
        article_publication = response.css('div.news-details-layout1 ul.post-info-dark>li>a::text').getall()
        item['author'] = article_publication[-3]        
        parsed_date = dateparser.parse(article_publication[-1])
        item['date_pub'] = self.__normalize_date(parsed_date)
        item['link'] = req_url
        item['topic'] = article_block.css('div.topic-box-sm::text').get()
        item['text_html'] = ' <br/> '.join(article_block.css('blockquote::text,p::text').getall())

        return item

