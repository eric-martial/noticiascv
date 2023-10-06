import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    topic = scrapy.Field()
    link = scrapy.Field()
