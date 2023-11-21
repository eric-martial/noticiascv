import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.santiagomagazine import SantiagoMagaZineSpider
from .spiders.anacao import anacao

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(anacao)
process.crawl(SantiagoMagaZineSpider)
process.start()