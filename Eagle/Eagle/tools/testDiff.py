import time
with open('testSetDiffMat.txt', 'r') as f:
	txt = f.readlines()

mid = int(len(txt)/2)
a = txt[0:mid]
b = txt[mid:-1]
timebegin = time.time()
print "begin diff at:", timebegin
c = list(set(a)-set(b))
timedone = time.time()
print 'done.time:', timedone
for i in c:
	print i
