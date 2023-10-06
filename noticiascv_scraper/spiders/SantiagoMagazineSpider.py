from ..items import ArticleItem
import scrapy
from urllib.parse import urlparse



class SantiagoMagaZineSpider(scrapy.Spider):
    name = "santiagomagazine"
    allowed_domains = ['santiagomagazine.cv']
    base_url = 'https://santiagomagazine.cv'
    start_urls = [
        'https://santiagomagazine.cv/economia'#,
        # 'https://santiagomagazine.cv/politica',
        # 'https://santiagomagazine.cv/cultura',
        # 'https://santiagomagazine.cv/diaspora',
        # 'https://santiagomagazine.cv/editorial',
        # 'https://santiagomagazine.cv/outros-mundos',
        # 'https://santiagomagazine.cv/sociedad'
    ]

    def parse(self, response):
        highlighted_article = response.css('.col-xl-12.col-lg-6.col-md-6.col-sm-12.mb-50')
        if highlighted_article:
            item = ArticleItem()
            item['title'] = highlighted_article.css('h3.title-semibold-dark a::text').get()
            item['link'] = highlighted_article.css('h3.title-semibold-dark a::attr(href)').extract_first()
            item['date'] = highlighted_article.css('div.post-date-dark ul li::text').getall()[-1]
            path_segments = urlparse(response.url).path.split('/')
            item['topic'] = path_segments[-1] if path_segments else None
            yield item
        
        for article in response.css('div.row div.media.media-none--lg'):
            item = ArticleItem()
            item['title'] = article.css('h3.title-semibold-dark a::text').get()
            item['link'] = article.css('h3.title-semibold-dark a::attr(href)').get()
            item['topic'] = article.css('div.topic-box-sm::text').get()
            item['date'] = article.css('div.post-date-dark ul li::text').get()
            yield item
        
        next_page = response.css('div.pagination-btn-wrapper li.page-item a::attr(href)').extract()[-1]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
