import tornado.ioloop
import tornado.web
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

class SpiderHandler(tornado.web.RequestHandler):
	websCashe = {}

	def get(self):
		name = self.get_argument("sitename")
		url = self.get_argument("siteurl")
		num = self.get_argument("count")
		if int(num) > 0:
			print "from:%s (%s) get:%s new items\n"%(name, url, num)
		self.write("tornado get it!")
		return


application = tornado.web.Application([
	(r"/message/new_message", SpiderHandler),
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()