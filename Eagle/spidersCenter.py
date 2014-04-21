from twisted.internet import reactor, task
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from Eagle.spiders.blackspider import BlackSpider
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ServerEndpoint

from pymongo import MongoClient
import time

def Singleton(cls):
	def wrap(*args, **kwargs):
		o = getattr(cls, "__instance__", None)
		if not o:
			o = cls(*args, **kwargs)
			cls.__instance__ = o
		return o
	return wrap

class TimerCrawler(object):
	def __init__(self, urls, time):
		self.urls = urls
		self.time = time
		self.timer = task.LoopingCall(self.onTimer)
		self.crawler = None
		#this indicate spiderclosed is allowed to restart crawler
		self.run = True

	def start(self):
		if self.crawler and self.crawler.engine.running:
			return False
		self.run = True
		self.timer.start(self.time)
		return True

	def stop(self):
		self.run = False
		if self.crawler and self.crawler.engine.running:
			self.crawler.stop()
		if self.timer.running:
			self.timer.stop()

	def onTimer(self):
		if not self.crawler or not self.crawler.engine.running:
			self.__crawl()
		else:
			#stop to wait for crawler finished
			self.timer.reset()
			self.timer.stop()

	def onEngineStop(self):
		log.msg("-------spider closed", level=log.INFO)
		self.crawler.signals.disconnect(self.onEngineStop, signal=signals.engine_stopped)
		if self.run and not self.timer.running:
			self.start()
			log.msg("-------restart timer", level=log.INFO)

	def __crawl(self):
		self.crawler = self.createCrawler(self.urls, self.time)
		self.crawler.signals.connect(self.onEngineStop, signal=signals.engine_stopped)
		self.crawler.start()

	def createCrawler(self, urls, priority):
		spider = BlackSpider(urls, priority)
		crawler = Crawler(Settings())
		crawler.configure()
		crawler.crawl(spider)
		return crawler

@Singleton
class CrawlerManager():
	commands = ["start", "stop"]

	def __init__(self):
		self.sites, self.sitePriDict, self.crawlerDict = self.__loadSites(), {}, {}
		self.timerDict = self.timerSignal = {}

		for item in self.sites:
			priority = getattr(item, "priority", 20)
			if not self.sitePriDict.has_key(priority):
				self.sitePriDict[priority] = []
			self.sitePriDict[priority].append(item["siteurl"])

		for p in self.sitePriDict.iterkeys():
			self.crawlerDict[p] = TimerCrawler(self.sitePriDict[p], p)

		log.start()

	def start(self, priority=None):
		if priority and not self.crawlerDict.has_key(int(priority)):
			return "priority has not found!"
		tostart = self.crawlerDict.values() if not priority else [self.crawlerDict[int(priority)]]
		fails = [str(crawler.time) for crawler in tostart if not crawler.start()]
		return "all crawlers started!" if not fails else "priority: "+",".join(fails)+" start fail!"

	def stop(self, priority=None):
		tostop = self.crawlerDict.values() if not priority else [self.crawlerDict[int(priority)]]
		for crawler in tostop:
			crawler.stop()
		return "crawler stopped!"

	def __loadSites(self):
		mongo = MongoClient()
		mongo.siteDb.authenticate("zql","fine")
		return [item for item in mongo.siteDb.siteCol.find({}, {"_id":0}).limit(10)]


class Commander(LineReceiver):
	def connectionMade(self):
		print "connection made"

	def connctionLost(self, reason):
		print "connection lost, reason:", reason

	def lineReceived(self, line):
		inputParms = line.split(" ")
		command = inputParms[0]
		args = inputParms[1:]
		if command in CrawlerManager().commands:
			if len(args) == 0:
				self.sendLine("response:"+getattr(CrawlerManager(), command)())
			else:
				self.sendLine("response:"+getattr(CrawlerManager(), command)(*args))

class ProFactory(Factory):
	protocol = Commander

reactor.listenTCP(8007, ProFactory())
reactor.run()