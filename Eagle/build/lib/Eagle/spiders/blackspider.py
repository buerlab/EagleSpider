
#this spider is for get title and url msg
#start_urls
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import Spider
from Eagle.items import TitleItem, TitleGroup
import Eagle.spiderUtils as utils
from pymongo import MongoClient
from scrapy import log
from scrapy.http import Request
from bs4 import BeautifulSoup

class BlackSpider(Spider):

    name = 'blackspider'

    def __init__(self, category=None, *args, **kwargs):
        super(BlackSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.crawledurls = []

        mongo = MongoClient()
        db = mongo.siteDb
        sites = db.siteCol.find()
        for site in sites:
            self.start_urls.append(site['siteurl'])
        mongo.close()

    
    # self.url_xpath_dic = utils.geturljson()
    # self.titleList = []
    # for url in self.url_xpath_dic:
    #     self.start_urls.append(url)

    def parse(self, response):
        log.msg("parsing%s"%response.url, level=log.INFO)
        sel = Selector(response)
        self.crawledurls.append(response.url)

        index = self.start_urls.index(response.url)
        # extract all <a> and pass to pipline
        allA = sel.xpath("//a").extract()
        titles = []
        for a in allA:
            a.encode("utf-8")
            soup = BeautifulSoup(a)
            if soup.a.attrs.has_key("href") and len(soup.a.text)>0 and len(soup.a["href"])>0:
                titles.append({"title":soup.a.text, "url":soup.a["href"]})

        yield TitleGroup(siteurl=response.url, titles=titles)



        

