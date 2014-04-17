import json

urlsjson = None

def geturljson():
	global urlsjson
	if urlsjson == None:
		with open("data/urls.json", "r") as f:
			urlsjson = json.load(f)
	return urlsjson


def lsurls():
	print geturljson()

def inserturl(url, titlePath, urlPath, tag):
	urlsjson = geturljson()
	path = {"title":titlePath, "url":urlPath, "tag":tag}
	if urlsjson.has_key(url):
		urlsjson[url].append(path)
	else:
		urlsjson[url] = [path]

	dump()

def remove(url):
	urlsjson = geturljson()
	del urlsjson[url]
	dump()

def clearall():
	global urlsjson
	urlsjson = {}
	dump()

def dump():
	with open("data/urls.json", "wb") as f:
		json.dump(geturljson(), f, ensure_ascii=False)

	

