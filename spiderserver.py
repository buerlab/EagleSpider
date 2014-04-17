import tornado.ioloop
import tornado.web
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

class SpiderHandler(tornado.web.RequestHandler):
	websCashe = {}

	def post(self):
		url = self.get_argument("url")
		num = self.get_argument("num")
		content = json.loads(self.get_argument("content"))
		if int(num) > 0:
			print "from:%s get:%s new items\n"%(url, num)
			for i in content:
				print i

		self.write("tornado get it!")
		return


application = tornado.web.Application([
	(r"/spider", SpiderHandler),
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()