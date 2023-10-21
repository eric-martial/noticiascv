from ..items import ArticleItem
import scrapy
import dateparser
from datetime import datetime
import html


class anacao(scrapy.Spider):
    name = "anacao"
    allowed_domains = ['anacao.cv']
    base_url = 'https://anacao.cv'
    start_urls = [
        'https://www.anacao.cv/categoria/sociedade/',
        'https://www.anacao.cv/categoria/politica/',
        'https://www.anacao.cv/categoria/cultura/',
        'https://www.anacao.cv/categoria/economia/',
        'https://www.anacao.cv/categoria/desporto/',
        'https://www.anacao.cv/categoria/mundo/',
        'https://www.anacao.cv/categoria/diaspora/'
    ]

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    async def parse(self, response):
        hero_urls = response.css('div#feat-top-wrap a::attr(href)').getall()
        page_urls = hero_urls + response.css('div#archive-list-wrap li>a::attr(href)').getall()

        for page_url in page_urls:
            page_url = response.urljoin(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse_news)

        next_page = response.css('div.pagination a::attr(href)').getall()[-2]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def __normalize_date(self, date_obj):
        if not isinstance(date_obj, datetime):
            return None
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    async def parse_news(self, response):
        req_url = response.url
        
        item = ArticleItem()

        item['source'] = self.name
        item['title'] = response.css('header#post-header h1::text').get()
        item['author'] = response.css('header#post-header span.author-name a::text').get()     
        parsed_date = dateparser.parse(response.css('header#post-header span.post-date time::text').get())
        item['date_pub'] = self.__normalize_date(parsed_date)
        item['link'] = req_url
        item['topic'] = response.css('header#post-header span::text').get()
        content_string = response.css('div#content-main p::text').getall()
        filtered_strings = [s.strip() for s in content_string if s.strip()]
        item['text_html'] = html.unescape(' <br/> '.join(filtered_strings))

        return item

