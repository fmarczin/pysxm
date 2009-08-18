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
"""File in/output support.

@author: fm
@version: $Rev: 123 $
"""
import sys,os
import fnmatch

def init():
    """Find all available format plugins.
    
    This function must be called before format plugins can be used.
    It can be called again to search for plugin modules again.     
    """
    # plugin directory relative to directory we run from:
    dirname = os.path.join(os.path.dirname(__file__),'FormatPlugins')
    
    for file in os.listdir(dirname):
        # find all files whose name end in "Plugin.py"
        if file[-9:] == "Plugin.py":
            f, e = os.path.splitext(file)
            try:
                sys.path.insert(0, dirname)
                try:
                    # try to import it
                    mod = __import__(f, globals(), locals(), [])
                finally:
                    del sys.path[0]
            except ImportError:
                print "Format: failed to import",
                print f, ":", sys.exc_value

def getFilterString(types=None):
    """Returns a filter string for known filetypes, suitable for QFileDialog.getOpenFileName.
    
    @keyword types: (optional) a list of data types from L{SXM.Data} to take into account
    @type types: list

    """
    return ';;'.join([("%s (%s)" % (r.description,' '.join(r.patterns))) for r in FormatReader.__subclasses__() if (not types) or (r.datatype in types)])
    
def findReaderForFilename(fname,types=None):
    """Returns a class derived from L{FormatReader} appropriate for reading fname.
    
    Right now, the first reader that claim()s the file gets it.

    @param fname: File to be read
    @type fname: string
    @keyword types: (optional) a list of data types from L{SXM.Data} to take into account
    @type types: list
    @raises FormatUnknownError:
    """
    for r in FormatReader.__subclasses__():
        if (not types) or (r.datatype in tuple(types)):
            if r().claim(fname):
                return r
    else:
        # no known reader claimed the file
        raise FormatUnknownError, 'Format of %s unknown' % fname

def fromFile(fname,types=None):                    
    """Returns a data object of appropriate type, ready for reading.
    
    @param fname: File to be read
    @type fname: string
    @keyword types: (optional) a list of data types from L{SXM.Data} to take into account
    @type types: list
    """
    root, ext = os.path.splitext(fname)
    path, base = os.path.split(root)

    shortname = base + ext
    r = findReaderForFilename(shortname,types)
    obj = r.datatype() # create an instance of the type that reader r can fill
    obj.setReader(r)
    obj.filename = fname
    return obj

def loadFile(fname):
    """Load SXM data from file fname."""
    return fromFile(fname).load()
        
class FileIOException(Exception):
    """Base-class for exceptions defined in this module."""
    pass

class FormatInvalidError(FileIOException):
    """Raised when reading of a file failed because of it being in the wrong format."""
    pass

class FormatUnknownError(FileIOException):
    """Raised when no appropriate format plugin can be found."""
    pass

class FormatReader(object):
    """Base class for file reading plugins.
    
    Readers in format plugins must be subclasses of this class. 
    
    @cvar format: A short format identifier string
    @type format: str
    @cvar description: A short format description
    @type description: str
    @cvar patterns: A tuple of filename patterns accepted by this reader
    @type patterns: Tuple
    @cvar datatype: The type of data (a class from L{SXM.Data}) this reader can read
    @type datatype: class
    """
    
    format = ''
    description = '' 
    patterns = ('*.*',)
    datatype = None
    
    def __init__(self): pass
        
    def claim(self,fname):
        """Returns True if this reader thinks it can read the file fname.
        
        This function may or may not take a look at the actual file given.
        This base class implements a simple version of the method which
        checks if the filename matches one of the filename patterns the
        plugins claims to know.
        
        @param fname: File to be tested
        @type fname: string
        @return: True if this reader can read the file, False otherwise
        """
        for pat in self.patterns:
            if fnmatch.fnmatch(fname,pat):
                return True
        return False
    
    def readData(self,data):
        """Reads the actual data for file fname and fills it into the data object.
                
        @param data: Data object to fill
        @type data: Any subclass of L{Data.DataField}
        @raise FormatInvalidError: When reading fails because the file has the wrong format.
        """
        pass
        
    def readHeader(self,data):
        """Reads just the header information for the data object.
        
        This is needed before reading the actual data, since most of the
        time the header specifies where to find the data.
        This function is also intended to provide fast access to a files 
        meta-data to be used in lists, previews etc.

        @param data: Data object to fill
        @type data: Any subclass of L{Data.DataField}
        @raise FormatInvalidError: When reading fails because the file has the wrong format.
        """
        pass

    
