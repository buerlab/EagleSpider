import sys
import httplib, urllib
import json
import time

scrapyd_address = "115.29.8.74:6800"
# scrapyd_address = "localhost:6800"
projname = "Eagle"
spidername = "blackspider"
jobid = ''

def start():
	while True:
		global jobid
		jobs = json.loads(ls())
		if jobs["status"] == "ok" and len(jobs["pending"])+len(jobs["running"]) == 0:
			print "jobs pending:%d"%len(jobs["pending"]), "runing:%d"%len(jobs["running"])
			headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
			parms = urllib.urlencode({"project":projname,"spider":spidername})
			conn = httplib.HTTPConnection(scrapyd_address)
			conn.request("POST","/schedule.json",parms,headers)
			resp = conn.getresponse()
			resBody = resp.read()
			resData = json.loads(resBody)
			jobid = resData["jobid"]
			print resp.status, resBody
		elif jobs["status"] == "error":
			print "list jobs error"

		time.sleep(10)

def cancel():
	jobs = json.loads(ls())
	jobToCancel = jobs["pending"]
	jobToCancel.extend(jobs["running"])
	for job in jobToCancel:
		conn = httplib.HTTPConnection(scrapyd_address)
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		parms = urllib.urlencode({"project":projname,"job":job["id"]})
		conn.request("POST","/cancel.json",parms, headers)
		response = conn.getresponse()
		print "cancel:",job["id"],":",response.status, response.read()
		conn.close()

def ls():
	conn = httplib.HTTPConnection(scrapyd_address)
	parms = urllib.urlencode({"'project'":projname})
	conn.request("GET", "/listjobs.json?project=Eagle")   # http://abc.com/listjob.json?'xxx'=yyy
	resp = conn.getresponse()
	print "get jobs:",resp.status
	result = resp.read()
	print result
	return result

if __name__ == "__main__":
	if sys.argv[1] == "start":
		start()
	elif sys.argv[1] == "cancel":
		cancel()
	elif sys.argv[1] == 'ls':
		ls()


