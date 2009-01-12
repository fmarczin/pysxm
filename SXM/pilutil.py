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
import Image

standardpal = {
               'grey':(
                 (  0, (  0,   0,   0)), # black
                 (255, (255, 255, 255)), # white
                 ),
               'jet':(
                 (  0, (  0,   0, 131)), # dark blue
                 ( 31, (  0,   0, 255)), # blue
                 ( 95, (  0, 255, 255)), # turqoise
                 (159, (255, 255,   0)), # yellow
                 (223, (255,   0,   0)), # red
                 (255, (128,   0,   0)), # dark red
                 )
               }

def palfrompoints(points):
    pal = []
    
    for n in range(len(points)-1):
        (indi,(ri,gi,bi)) = points[n]
        (indf,(rf,gf,bf)) = points[n+1]
        nind = indf - indi
        (dr,dg,db) = (float(rf - ri)/float(nind), float(gf - gi)/float(nind), float(bf - bi)/float(nind))
        
        for i in range(nind):
            pal.extend((int(round(ri + (dr*i))), int(round(gi + (dg*i))), int(round(bi + (db*i)))))
        
    pal.extend((rf,gf,bf))
    assert len(pal) == 768
    return pal
            
def stdpal(name):
    return palfrompoints(standardpal[name])
