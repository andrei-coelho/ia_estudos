from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.NetshoesSpider import NetshoesSpider

settings = get_project_settings()
settings.set('DOWNLOAD_DELAY', 3) 
settings.set('AUTOTHROTTLE_ENABLED', True)
settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')  # Defina o USER_AGENT

process = CrawlerProcess(settings)

process.crawl(NetshoesSpider)
process.start() 