from twisted.internet import reactor
from scrapy.crawler import crawler
from scrapy.setting import Settings
from scrapy import log
from spiders.blackspider import BlackSpider

spider = BlackSpider()
crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run()