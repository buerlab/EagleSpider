from scrapy import signals
from scrapy.exceptions import NotConfigured
import time
from scrapy import log
import pickle
from pymongo import MongoClient

class CrawlTimeRecord(object):

	def __init__(self):
		self.beginTime = 0

	@classmethod
	def from_crawler(cls, crawler):
		obj = cls()

		crawler.signals.connect(obj.record, signal=signals.spider_opened)
		crawler.signals.connect(obj.recDone, signal=signals.spider_closed)
		return obj

	def record(self, spider):
		self.beginTime = time.time()

	def recDone(self, spider):
		recordTime = time.time()-self.beginTime
		log.msg("-------------time total:%d"%recordTime, level=log.INFO)
		mongo = MongoClient()
		mongo.timeRecordDb.recordCol.insert({"time":recordTime})
		mongo.close()

class ErrorCatcher(object):
	@classmethod
	def from_crawler(cls, crawler):
		obj = cls()

		crawler.signals.connect(obj.onError, signal=signals.spider_error)
		return obj

	def onError(self, failure, resp, spider):
		print "-------error catch"
		print failure
		print resp
		print spider.name

