#! /usr/bin/python

import sys
import pickle
import jieba

def getStoragePath():
	return "hounddata"

trainTxt = ''
currMatName =  None
currTrain = {}
def setFileTxt(fileName):
	global trainTxt

	with open(fileName, 'r') as f:
		trainTxt = ''.join(f.readlines())
	print trainTxt

def train():
	global currTrain
	global trainTxt

	wordList = jieba.cut(trainTxt, cut_all = False)
	currTrain = {}
	currTrain['lines'] = len(wordList)
	data = {}
	for word in wordList:
		if data.has_key(word):
			data[word] += 1
		else:
			data[word] = 1
	currTrain['data'] = data

def filtN(num):
	global currTrain

	delKeys = []
	for key in currTrain:
		if currTrain[key] <= num:
			delKeys.append(key)
	for delKey in delKeys:
		del currTrain[delKey]
	print 'delete',len(delKeys),'items'
	dump()

def filtK(*keys):
	global currTrain

	for key in keys:
		if currTrain.has_key(key):
			del currTrain[key]
			print 'delete',key
		else:
			print key,'is not exist'


def show(matname = None, sortReverse = True):
	global currTrain
	
	if matname:
		print 'get data from mat......'
		currMatName = matname
		currTrain = getTrainModel(matname)
	else:
		print 'print currTran......'

	sort = sorted(currTrain.items(),key = lambda item:item[1], reverse = sortReverse)
	for item in sort:
		output = ''
		for i in range(item[1]):
			output += '+'
		output += ':'+item[0]+" "+str(item[1])
		print output

def getTrainModel(matname):
	with open(getStoragePath()+'/'+matname, 'r') as f:
		model = pickle.load(f)
	return model

def dump(matname = None):
	global currTrain
	name = matname or currMatName
	if name:
		with open(getStoragePath()+'/'+matname, 'w') as f:
			dataString = pickle.dump(currTrain, f)

def check(matname, source):
	return True








