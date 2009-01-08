import os
import sys
import time
from syck import *
from pylab import *
from SXM import SM3
from SXM import Omikron

for filename in sys.argv[1:]:
	filename = os.path.normpath(os.path.join(os.getcwd(),filename))
	print 'reading ' + filename + '...'
	try:
		fstat = os.stat(filename)
		f = open(filename,'rb')
		try:
			pages = []
			nimages = 0
			while not (f.tell() == fstat.st_size):
				pages.append(SM3.read_page(f))
				if pages[-1]['type'] == SM3.TImage:
					nimages += 1
				print 'read 1 page. ' + str(f.tell()) + ' of ' + str(fstat.st_size) + ' bytes'
#				print dump(pages[-1])
		finally:
			f.close()
	except IOError:
		print "Could not read from %s" % filename
	if nimages > 0:
		Omikron.write(filename,pages)
	d = open('dump','w')
	for p in pages:
		d.write(dump(p))
	d.close()
#	time.sleep(5)

