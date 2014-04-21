#coding=utf8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import uuid

from items import TitleItem, TitleGroup
import libs.hound
import config
from bs4 import BeautifulSoup
from pymongo import MongoClient
from scrapy import log
import json
import httplib, urllib
import urlparse
import time


class FilterPipeline(object):
	def process_item(self, item, spider):
		#filter the invalid item
		toRemove = []
		for t in item["titles"]:
			if len(t["title"])==0:
				toRemove.append(t)

		for rm in toRemove:
			item["titles"].remove(rm)
		return item

class UrlFullFillPipeline(object):
	def process_item(self, item, spider):
		for t in item["titles"]:
			if not urlparse.urlparse(t["url"]).scheme:
				t["url"] = urlparse.urljoin(item["siteurl"], t["url"])
		return item


class DuplicatedPipeline(object):

	def process_item(self, item, spider):
		log.msg("procesing deplicatedpipeline..............", level=log.INFO)
		siteurl = item['siteurl']

		mongo = MongoClient()
		sitename = mongo.siteDb.siteCol.find_one({"siteurl":siteurl})["sitename"]

		db = mongo.spiderDb
		find = db.snapshotCol.find_one({"siteurl":siteurl}, {"_id":0, "titles":1}) or {"titles":[]}

		titlesfromdb = [piece["title"] for piece in find["titles"]]
		titlesfromspi = [piece["title"] for piece in item["titles"]]
		#newItems: ["title"]
		newItems = list(set(titlesfromspi)-set(titlesfromdb))
		
		log.msg("----------get new:%d"%len(newItems), level=log.INFO)
		if len(newItems)>0:
			#if any new found, update db to the new
			db.snapshotCol.update({"siteurl":siteurl}, {"$set":{"updatetime":time.time()}}, True)
			db.snapshotCol.update({"siteurl":siteurl}, {"$set":{"titles":item["titles"]}}, True)
			db.crawltitleCol.update({"siteurl":siteurl}, {"$set":{"updatetime":time.time()}}, True)
			#insert the newitems into db
			for piece in newItems:
				for piece2 in item["titles"]:
					if piece2["title"] == piece:
						db.crawltitleCol.update({"siteurl":siteurl}, {"$push":{"titles":{"title":piece, "url":piece2["url"], "isnew":True}}}, True)
						break

			# send a new items msg to server
			conn = httplib.HTTPConnection("localhost:8888")
			try:
				parms = urllib.urlencode({"sitename":sitename,"siteurl":siteurl,"count":len(newItems)})
				conn.request("GET","/message/new_message?%s"%parms)
				resp = conn.getresponse()
				log.msg("send to server:%d, get:%s"%(resp.status,resp.read()))
			except:
				log.msg("-------send update message to server error!!!", level=log.INFO)
			finally:
				conn.close()

		mongo.close()
		
		return item

