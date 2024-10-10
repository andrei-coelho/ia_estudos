import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.NetshoesSpider import NetshoesSpider

chromedriver_path = os.path.join(os.getcwd(), 'chromedriver')

settings = get_project_settings()
#settings.set('SELENIUM_DRIVER_NAME', 'chrome') 
#settings.set('SELENIUM_DRIVER_EXECUTABLE_PATH', chromedriver_path) 
#settings.set('SELENIUM_DRIVER_ARGUMENTS', ['--headless', '--no-sandbox', '--disable-dev-shm-usage']) 


settings.set('DOWNLOAD_DELAY', 3) 
settings.set('AUTOTHROTTLE_ENABLED', True)
settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
settings.set('DOWNLOADER_MIDDLEWARES', {
    'scrapy_selenium.SeleniumMiddleware': 800,
})

process = CrawlerProcess(settings)

process.crawl(NetshoesSpider)
process.start() 