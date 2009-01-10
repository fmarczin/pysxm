#
# simple testing file - no unit test
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
