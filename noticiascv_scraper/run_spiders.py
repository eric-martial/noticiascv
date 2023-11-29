import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.santiagomagazine import SantiagoMagaZineSpider
from .spiders.anacao import AnacaoSpider

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(AnacaoSpider)
process.crawl(SantiagoMagaZineSpider)
process.start()