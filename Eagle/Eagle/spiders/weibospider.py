from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from Eagle.items import EagleItem
# import scrapy.http.Request

class WeibospiderSpider(Spider):
    name = 'weibospider'
    start_urls = ['http://weibo.com/u/1604372251/home?wvr=5']

    def make_requests_from_url(u):
        return Request(url=u, cookies={""})

    def parse(self, response):
        pass
        # print "passing........................"
        # sel = Selector(response)
        # allA = sel.xpath("//a/text()").extract()
        # weiboInfo = sel.xpath("//div[@class='WB_info']//text()").extract()
        # weiboCnt = sel.xpath("//div[@class='WB_text']//text()").extract()

        # for a in allA:
        #     print a

        # for i in range(len(weiboInfo)):
        #     print weiboInfo[i]
        #     print weiboCnt[i]
