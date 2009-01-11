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
#
# simple testing file - no unit test
#
import os
import SXM

os.chdir('c:/arbeit/inmnas/data/topsdos/20060907')
import os
i = SXM.open('xt050h00.001').bgPlaneSubtract()
i.saveImage('test.png',pal='jet')

l = [SXM.FileIO.fromFile('xt050h00.0%i1' % (n)).load() for n in range(9)]
i = l[0]
i.bgPlaneSubtract()
i.saveImage('test.png',pal='jet')
