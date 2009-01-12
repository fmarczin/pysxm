<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet ekr_test?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.278125">
	<global_window_position top="94" left="1372" height="986" width="1280"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="fmarczin.20080910183207.6" a="E" tnodeList="fmarczin.20080910183207.6,fmarczin.20080910183207.7,fmarczin.20080910183207.8,fmarczin.20080910183207.9,fmarczin.20080910183207.10,fmarczin.20080910183207.11,fmarczin.20080910183207.12,fmarczin.20080910183207.13,fmarczin.20080910183207.14,fmarczin.20080910224433.2,fmarczin.20080910183207.15,fmarczin.20080910224433.3,fmarczin.20080910183207.16,fmarczin.20080910183207.17,fmarczin.20080910183207.18,fmarczin.20080910183207.19,fmarczin.20080910183207.20,fmarczin.20080910183207.21,fmarczin.20080910183207.22,fmarczin.20080910183207.23,fmarczin.20080910183207.24,fmarczin.20080910183207.25,fmarczin.20080910183207.26,fmarczin.20080910183207.27,fmarczin.20080910183207.28,fmarczin.20080910183207.29,fmarczin.20080910183207.30,fmarczin.20080910183207.31,fmarczin.20080910183207.32,fmarczin.20080910183207.33,fmarczin.20080910183207.34,fmarczin.20080910183207.35,fmarczin.20080910183207.36,fmarczin.20080910183207.37" str_leo_pos="0"><vh>@file D:\Arbeit\SXM\SXM\Data.py</vh>
<v t="fmarczin.20080910183207.7"><vh>Data declarations</vh></v>
<v t="fmarczin.20080910183207.8" a="E"><vh>class DataField</vh>
<v t="fmarczin.20080910183207.9"><vh>__init__</vh></v>
<v t="fmarczin.20080910183207.10"><vh>dataChanged</vh></v>
<v t="fmarczin.20080910183207.11"><vh>updateDataRange</vh></v>
<v t="fmarczin.20080910183207.12"><vh>setReader</vh></v>
<v t="fmarczin.20080910183207.13"><vh>findReader</vh></v>
<v t="fmarczin.20080910183207.14" a="E"><vh>loadHeader</vh>
<v t="fmarczin.20080910224433.2"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
</v>
<v t="fmarczin.20080910183207.15" a="E"><vh>loadData</vh>
<v t="fmarczin.20080910224433.3"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
</v>
<v t="fmarczin.20080910183207.16"><vh>load</vh></v>
</v>
<v t="fmarczin.20080910183207.17" a="E"><vh>class G1D</vh>
<v t="fmarczin.20080910183207.18"><vh>__init__</vh></v>
</v>
<v t="fmarczin.20080910183207.19"><vh>class G2D</vh>
<v t="fmarczin.20080910183207.20"><vh>__init__</vh></v>
<v t="fmarczin.20080910183207.21"><vh>bgRowwiseZOffset</vh></v>
<v t="fmarczin.20080910183207.22"><vh>bgColwiseZOffset</vh></v>
<v t="fmarczin.20080910183207.23"><vh>bgPlaneSubtract</vh></v>
<v t="fmarczin.20080910183207.24"><vh>savePNG</vh></v>
<v t="fmarczin.20080910183207.25"><vh>saveImage</vh></v>
<v t="fmarczin.20080910183207.26"><vh>toImage</vh></v>
</v>
<v t="fmarczin.20080910183207.27" a="E"><vh>class G3D</vh>
<v t="fmarczin.20080910183207.28"><vh>__init__</vh></v>
</v>
<v t="fmarczin.20080910183207.29" a="E"><vh>class LockInData</vh>
<v t="fmarczin.20080910183207.30"><vh>__init__</vh></v>
</v>
<v t="fmarczin.20080910183207.31" a="E"><vh>class Spectroscopy</vh>
<v t="fmarczin.20080910183207.32"><vh>__init__</vh></v>
</v>
<v t="fmarczin.20080910183207.33" a="E"><vh>class Image</vh>
<v t="fmarczin.20080910183207.34"><vh>__init__</vh></v>
<v t="fmarczin.20080910183207.35"><vh>__repr__</vh></v>
</v>
<v t="fmarczin.20080910183207.36" a="E"><vh>class SpecField</vh>
<v t="fmarczin.20080910183207.37"><vh>__init__</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="fmarczin.20080910183207.6">@language python
@tabwidth -4
@others
</t>
<t tx="fmarczin.20080910183207.7">"""Data types and functions.
@author: fm
@version: $Rev: 123 $
"""
import os
import scipy
import scipy.linalg
import FileIO
import pilutil

</t>
<t tx="fmarczin.20080910183207.8">class DataField(object):
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
    @others
</t>
<t tx="fmarczin.20080910183207.9">
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

</t>
<t tx="fmarczin.20080910183207.10">def dataChanged(self):
    self.updateDataRange()
    try:
        super(DataField, self).dataChanged(self)
    except AttributeError:
        pass

</t>
<t tx="fmarczin.20080910183207.11">def updateDataRange(self):
    """Update the values of dataMax and dataMin, call this after changing the data."""
    if self.d != None:
        self.dataMax = self.d.max()
        self.dataMin = self.d.min()
    return self

</t>
<t tx="fmarczin.20080910183207.12">def setReader(self,reader):
    """Set the reader class."""
    self.Reader = reader()

</t>
<t tx="fmarczin.20080910183207.13">def findReader(self):
    """Find a reader class from available format plugins for our filename."""
    reader = FileIO.findReaderForFilename(self.filename)
    self.setReader(reader)

</t>
<t tx="fmarczin.20080910183207.14">def loadHeader(self,force=False):
    &lt;&lt; docstring &gt;&gt;
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

</t>
<t tx="fmarczin.20080910183207.15">def loadData(self,force=False):
    &lt;&lt; docstring &gt;&gt;
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

</t>
<t tx="fmarczin.20080910183207.16">def load(self):
    """Read data from file.

    Convenience method. Just calls L{loadData}.
    """
    self.loadData()
    return self

</t>
<t tx="fmarczin.20080910183207.17">class G1D(DataField):
    """General 1-dimensional data.

    This is mainly intended as a base class.
    This class should implement methods common to 1-dimensional data types
    """
    @others
</t>
<t tx="fmarczin.20080910183207.18">
def __init__(self):
    super(G1D,self).__init__()

</t>
<t tx="fmarczin.20080910183207.19">class G2D(DataField):
    """General 2-dimensional data.

    This is mainly intended as a base class.
    This class should implement methods common to 2-dimensional data types

    @ivar XRes: Number of datapoints in X-direction
    @type XRes: number
    @ivar YRes: Number of datapoints in Y-direction
    @type YRes: number
    """
    @others
</t>
<t tx="fmarczin.20080910183207.20">
def __init__(self):
    super(G2D,self).__init__()
    self.XRes = 0
    self.YRes = 0

</t>
<t tx="fmarczin.20080910183207.21">def bgRowwiseZOffset(self):
    """Subtract each row's mean value from it.
    """
    # make a vector of rowwise mean values:
    rows = self.d.mean(1)
    # subtract from data:
    self.d = self.d - rows[:,scipy.newaxis]
    self.updateDataRange()
    return self

</t>
<t tx="fmarczin.20080910183207.22">def bgColwiseZOffset(self):
    """Subtract each column's mean value from it.
    """
    # make a vector of colwise mean values:
    rows = self.d.mean(0)
    # subtract from data:
    self.d = self.d - rows[:]
    self.updateDataRange()
    return self

</t>
<t tx="fmarczin.20080910183207.23">def bgPlaneSubtract(self):
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

</t>
<t tx="fmarczin.20080910183207.24">def savePNG(self,cmin=None,cmax=None,pal='grey'):
    self.saveImage(self.filename + '.png', cmin=cmin, cmax=cmax, pal=pal)

</t>
<t tx="fmarczin.20080910183207.25">def saveImage(self,fname,cmin=None,cmax=None,pal='grey'):
    format = os.path.splitext(fname)[1][1:]
    savefile = open(fname,'wb')
    self.toImage(savefile,format=format,cmin=cmin,cmax=cmax,pal=pal)
    savefile.close()

</t>
<t tx="fmarczin.20080910183207.26">def toImage(self,fobj,format="bmp",cmin=None,cmax=None,pal='grey'):
    img = scipy.misc.pilutil.toimage(self.d,cmin=cmin,cmax=cmax)
    palette = pilutil.stdpal(pal)
    img.putpalette(palette)
    img.save(fobj, format)

</t>
<t tx="fmarczin.20080910183207.27">class G3D(DataField):
    """General 3-dimensional data.

    This is mainly intended as a base class.
    This class should implement methods common to 3-dimensional data types
    """
    @others
</t>
<t tx="fmarczin.20080910183207.28">
def __init__(self):
    super(G3D,self).__init__()

</t>
<t tx="fmarczin.20080910183207.29">class LockInData(object):
    """Class for lock-in measurements."""
    @others
</t>
<t tx="fmarczin.20080910183207.30">
def __init__(self):
    self.LIMod = None #: Lock-In modulation amplitude
    self.LIOff = None #: Lock-In offset
    self.LIPhase = None #: Lock-In Phase
    self.LISens = None #: Lock-In sensitivity
    self.LITau = None #: Lock-In time constant

</t>
<t tx="fmarczin.20080910183207.31">class Spectroscopy(object):
    """Class for spectroscopy measurements."""
    @others
</t>
<t tx="fmarczin.20080910183207.32">def __init__(self):
    self.SamplesT = None #: samples per curve, trace
    self.SamplesR = None #: samples per curve, retrace

</t>
<t tx="fmarczin.20080910183207.33">class Image(G2D,LockInData):
    """Base class for SXM images.
    """
    @others
</t>
<t tx="fmarczin.20080910183207.34">
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

</t>
<t tx="fmarczin.20080910183207.35">def __repr__(self):
    return "&lt;SPMImage %s %ix%inm %ix%ipx U:%.2fV I:%.2f1nA %s&gt;" % (self.ImageType,self.XSize,self.YSize,self.XRes,self.YRes,self.UBias,self.ISet,self.Name)

</t>
<t tx="fmarczin.20080910183207.36">class SpecField(G3D,LockInData):
    """Base class for spectroscopy fields.
    """
    @others
</t>
<t tx="fmarczin.20080910183207.37">
def __init__(self):
    super(SpecField,self).__init__()

</t>
<t tx="fmarczin.20080910224433.2">"""Load the header.

This function reads the header information from the file given in this 
object's filename attribute. If the header has been read before, it will
only be read again if C{force} is True. 

For reading, the L{readHeader&lt;SXM.FileIO.FormatReader.readHeader&gt;} 
method of our L{Reader} is called. If no Reader is set, L{findReader} is 
called to find one.

@keyword force: Set to True if header should be read even if it was already read before.
@type force: bool
"""</t>
<t tx="fmarczin.20080910224433.3">"""Load the data.

This function reads the actual data from the file given in this 
object's filename attribute. If the data has been read before, it will
only be read again if C{force} is True. Since the header information
is needed for reading the data, loadHeader will be called if the header
has not been read.

For reading, the L{readData&lt;SXM.FileIO.FormatReader.readData&gt;} 
method of our L{Reader} is called. If no Reader is set, L{findReader} is 
called to find one.

@keyword force: Set to True if data should be read even if it was already read before.
@type force: bool
"""</t>
</tnodes>
</leo_file>
