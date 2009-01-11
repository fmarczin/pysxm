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

"""Data types and functions.
@author: fm
@version: $Rev: 123 $
"""
import os
import scipy
import scipy.linalg
import FileIO
import pilutil

class DataField(object):
    """Base class for physical data.

    This class should implement methods common to *all* data types.
    The actual data is a scipy array

    @ivar d: THE DATA
    @type d: scipy.ndarray
    @ivar Name: A name for this dataset, roughly the filename
    @type Name: str
    @ivar filename: Name of the file this objecet was read from
    @type filename: str
    @ivar dataMax: maximum value of the data
    @type dataMax: number
    @ivar dataMin: minimum value of the data
    @type dataMin: number
    @ivar ZScale:  physical unit (nm,nA,V) per data unit
    @type ZScale: number
    @ivar ZUnit: physical unit of the data 'nm','nA', or 'V'
    @type ZUnit: str
    @ivar Reader: the reader class that can read our data
    @type Reader: class
    @ivar headerLoaded: has the header been read?
    @type headerLoaded: bool
    @ivar dataLoaded:  has the data been read? 
    @type dataLoaded: bool
    """

    def __init__(self,data=None):
        super(DataField,self).__init__()
        self.d = scipy.array(data) #: initialized from the optional parameter
        self.Name = "" 
        self.filename = None
        self.dataMax = None
        self.dataMin = None
        self.ZScale = None
        self.ZUnit = None
        self.Reader = None
        self.headerLoaded = False
        self.dataLoaded = False
        self.Temperature = None       

    def dataChanged(self):
        self.updateDataRange()
        try:
            super(DataField, self).dataChanged(self)
        except AttributeError:
            pass

    def updateDataRange(self):
        """Update the values of dataMax and dataMin, call this after changing the data."""
        if self.d != None:
            self.dataMax = self.d.max()
            self.dataMin = self.d.min()
        return self

    def setReader(self,reader):
        """Set the reader class."""
        self.Reader = reader()

    def findReader(self):
        """Find a reader class from available format plugins for our filename."""
        reader = FileIO.findReaderForFilename(self.filename)
        self.setReader(reader)

    def loadHeader(self,force=False):
        """Load the header.

        This function reads the header information from the file given in this 
        object's filename attribute. If the header has been read before, it will
        only be read again if C{force} is True. 

        For reading, the L{readHeader<SXM.FileIO.FormatReader.readHeader>} 
        method of our L{Reader} is called. If no Reader is set, L{findReader} is 
        called to find one.

        @keyword force: Set to True if header should be read even if it was already read before.
        @type force: bool
        """
        if self.Reader == None:
            self.findReader()
        if force or not self.headerLoaded:
            try:
                # try-except is to ensure that self.header_read is only set
                # if reading was successful
                self.Reader.readHeader(self)
                self.headerLoaded = True
            except:
                raise
        return self

    def loadData(self,force=False):
        """Load the data.

        This function reads the actual data from the file given in this 
        object's filename attribute. If the data has been read before, it will
        only be read again if C{force} is True. Since the header information
        is needed for reading the data, loadHeader will be called if the header
        has not been read.

        For reading, the L{readData<SXM.FileIO.FormatReader.readData>} 
        method of our L{Reader} is called. If no Reader is set, L{findReader} is 
        called to find one.

        @keyword force: Set to True if data should be read even if it was already read before.
        @type force: bool
        """
        if force or not self.dataLoaded:
            if force or not self.headerLoaded:
                self.loadHeader(force)
            try:
                # try-except is to ensure that self.header_read is only set
                # if reading was successful
                self.Reader.readData(self)
                self.dataLoaded = True
                self.updateDataRange()
            except:
                raise
        return self

    def load(self):
        """Read data from file.

        Convenience method. Just calls L{loadData}.
        """
        self.loadData()
        return self

class G1D(DataField):
    """General 1-dimensional data.

    This is mainly intended as a base class.
    This class should implement methods common to 1-dimensional data types
    """

    def __init__(self):
        super(G1D,self).__init__()

class G2D(DataField):
    """General 2-dimensional data.

    This is mainly intended as a base class.
    This class should implement methods common to 2-dimensional data types

    @ivar XRes: Number of datapoints in X-direction
    @type XRes: number
    @ivar YRes: Number of datapoints in Y-direction
    @type YRes: number
    """

    def __init__(self):
        super(G2D,self).__init__()
        self.XRes = 0
        self.YRes = 0

    def bgRowwiseZOffset(self):
        """Subtract each row's mean value from it.
        """
        # make a vector of rowwise mean values:
        rows = self.d.mean(1)
        # subtract from data:
        self.d = self.d - rows[:,scipy.newaxis]
        self.updateDataRange()
        return self

    def bgColwiseZOffset(self):
        """Subtract each column's mean value from it.
        """
        # make a vector of colwise mean values:
        rows = self.d.mean(0)
        # subtract from data:
        self.d = self.d - rows[:]
        self.updateDataRange()
        return self

    def bgPlaneSubtract(self):
        """Subtract a plane.

        Fits a least-squares-fitted plane to the data and subtracts it.
        """ 
        # subtract a least squares fitted plane
        # Z = a1*X + a2*Y + a3
        # the fit and the plane subtraction are done in float-land
        oldtype = self.d.dtype.char
        # create x and y vectors:
        [x,y] = scipy.array(scipy.mgrid[0:self.d.shape[0],0:self.d.shape[1]],dtype='f')
        vx, vy = x.ravel(), y.ravel()
        # build factor matrix ([vx] [vy] [1])
        a = scipy.column_stack([vx,vy, scipy.ones_like(vx)]).astype('f')
        d = scipy.array(self.d,dtype='f')
        # find least squares fit:
        coeff, resid, rank, s = scipy.linalg.lstsq(a,d.ravel())
        self.d = scipy.array(d - (x*coeff[0] + y*coeff[1] + coeff[2])).astype(oldtype)
        self.updateDataRange()
        return self

    def savePNG(self,cmin=None,cmax=None,pal='grey'):
        self.saveImage(self.filename + '.png', cmin=cmin, cmax=cmax, pal=pal)

    def saveImage(self,fname,cmin=None,cmax=None,pal='grey'):
        format = os.path.splitext(fname)[1][1:]
        savefile = open(fname,'wb')
        self.toImage(savefile,format=format,cmin=cmin,cmax=cmax,pal=pal)
        savefile.close()

    def toImage(self,fobj,format="bmp",cmin=None,cmax=None,pal='grey'):
        img = scipy.misc.pilutil.toimage(self.d,cmin=cmin,cmax=cmax)
        palette = pilutil.stdpal(pal)
        img.putpalette(palette)
        img.save(fobj, format)

class G3D(DataField):
    """General 3-dimensional data.

    This is mainly intended as a base class.
    This class should implement methods common to 3-dimensional data types
    """

    def __init__(self):
        super(G3D,self).__init__()

class LockInData(object):
    """Class for lock-in measurements."""

    def __init__(self):
        self.LIMod = None #: Lock-In modulation amplitude
        self.LIOff = None #: Lock-In offset
        self.LIPhase = None #: Lock-In Phase
        self.LISens = None #: Lock-In sensitivity
        self.LITau = None #: Lock-In time constant

class Spectroscopy(object):
    """Class for spectroscopy measurements."""
    def __init__(self):
        self.SamplesT = None #: samples per curve, trace
        self.SamplesR = None #: samples per curve, retrace

class Image(G2D,LockInData):
    """Base class for SXM images.
    """

    def __init__(self):
        super(Image,self).__init__()
        self.ImageType = "" # topo, dIdU, etc.
        self.Method = "" # (STM, AFM, etc.)
        self.UBias = 0
        self.ISet = 0
        self.XPos = 0 # offset of the image *center*
        self.YPos = 0
        self.XSize = 0
        self.YSize = 0
        self.ScanSpeed = 0 # nm/s
        self.Angle = 0

    def __repr__(self):
        return "<SPMImage %s %ix%inm %ix%ipx U:%.2fV I:%.2f1nA %s>" % (self.ImageType,self.XSize,self.YSize,self.XRes,self.YRes,self.UBias,self.ISet,self.Name)

class SpecField(G3D,LockInData):
    """Base class for spectroscopy fields.
    """

    def __init__(self):
        super(SpecField,self).__init__()

