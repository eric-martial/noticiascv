from ..items import ArticleItem
import scrapy
import dateparser
from datetime import datetime


class anacao(scrapy.Spider):
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

    