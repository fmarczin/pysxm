# Copyright 2008 Felix Marczinowski <fmarczin@physnet.uni-hamburg.de>
#
# This file is part of PySXM.
#
#    PySXM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    PySXM is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with PySXM.  If not, see <http://www.gnu.org/licenses/>.
#
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

