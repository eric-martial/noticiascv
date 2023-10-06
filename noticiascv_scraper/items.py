import scrapy


class ArticleItem(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    date_pub = scrapy.Field()
    text_html = scrapy.Field()
    topic = scrapy.Field()
    link = scrapy.Field()
