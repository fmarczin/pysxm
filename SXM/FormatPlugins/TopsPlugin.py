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
"""Plugin for reading TOPS files.

The module reads files produced by the old DOS-based software, as well as 
those produced by the newer Linux-based version.

@todo: This module must be improved to also read dI/dU and I images, as well as point- and lattice spectra    
@version: $Rev: 82 $
"""
from SXM import Data,FileIO
import scipy
import os
import re
import cStringIO
from decimal import Decimal
import math

class TopsTopoReader(FileIO.FormatReader):
    """Reader for the TOPS 2D images.
    
    Only height images are tested right now.
    """
    description = 'Tops Topography'
    format = 'TOPSTopo'
    patterns = ('?t*.*',)
    datatype = Data.Image
    
    def __init__(self):
        FileIO.FormatReader.__init__(self)
        self._header = []
        
    def claim(self,fname):
        match = re.match('^.t.*\.\d{3}$',fname,re.IGNORECASE)
        if match:
            return True
        else:
            return False

    def readHeader(self,ob):
        root, ext = os.path.splitext(ob.filename)
        path, base = os.path.split(root)
        
        ob.Name = base + ext
        ob.Method = 'STM'
        
        f = open(ob.filename)
        chunk = cStringIO.StringIO(f.read(16384))
    
        header = _topsParseHeader(chunk)
        
        # attach the header structure to our instance for later use:
        self._header = header
        
        try:
            # todo: is it really first x then y? Do they ever differ?
            ob.XRes, ob.YRes = [Decimal(n) for n in header['STM image list']['Samps/line'].split(' ')]
            ob.ImageType = {'Height':'Height',
                            'Current':'Current',
                            'DI/DX':'DI/DX'}[header['STM image list']['Image data']]
            ob.UBias = Decimal(header['Stm list']['Bias']) / Decimal('3276.8')
            # As far as I can see, old and new software always write 0 nA here:
            ob.ISet = Decimal(header['Stm list']['Setpoint'].split(' ')[0])
            ob.Angle = Decimal(str(math.degrees(float(header['Stm list']['Rotate Ang.']))))
            
            # fill out the Z-sensitivity field, depending on type of data
            if ob.ImageType == 'Height':
                ob.ZScale = Decimal(header['Microscope list']['Z sensitivity']) # nm/V
                ob.ZScale = ob.ZScale * Decimal('20.0') / Decimal('3276.8') # HV gain: 20
                ob.ZUnit = 'nm'
            if ob.ImageType == 'Current':
                ob.ZScale = Decimal('1000.0') / Decimal('3276.8')
                ob.ZUnit = 'nA'
            if ob.ImageType == 'DI/DX':
                ob.ZScale = Decimal('1.0') / Decimal('3276.8')
                ob.ZUnit = 'V'
            
            ob.XPos = Decimal(header['Stm list']['X offset'].split(' ')[0])
            ob.YPos = Decimal(header['Stm list']['Y offset'].split(' ')[0])
            ob.XSize = Decimal(header['Stm list']['Scan size'].split(' ')[0])
            ob.YSize = ob.XSize
        except KeyError, exc:
            raise FileIO.FormatInvalidError, "Missing data: %s" % (exc)
        
        # failure on these fields is not fatal:
        try:
            ob.Temperature = Decimal(header['Stm list']['Temperature'])
        except KeyError:
            pass
        
        f.close()

    def readData(self,ob):
        f = open(ob.filename,'rb')
        f.seek(int(self._header['STM image list']['Data offset']))
        data = f.read(int(self._header['STM image list']['Data length']))
        ob.d = scipy.fromstring(data,dtype=scipy.int16)
        ob.d.shape = ob.XRes, ob.YRes
        ob.d = scipy.flipud(ob.d)

class TopsSpecFieldReader(FileIO.FormatReader):
    """Reader for TOPS Spectroscopy fields.
    """
    description = 'Tops Spectroscopy'
    format = 'TOPSSpec'
    patterns = ('?l*.*',)
    datatype = Data.SpecField
    
    def __init__(self):
        FileIO.FormatReader.__init__(self)
        self._header = []
        
    def claim(self,fname):
        match = re.match('^.l.*\.\d+[abc]$',fname,re.IGNORECASE)
        if match:
            return True
        else:
            return False

    def readHeader(self,ob):
        """Reads the header into the given object.
        
        @param ob: The object to be filled.
        @type ob: L{SXM.Data.SpecField}
        """
        root, ext = os.path.splitext(ob.filename)
        path, base = os.path.split(root)
        
        ob.Name = base + ext
        ob.Method = 'STM'
        
        f = open(ob.filename)
        chunk = cStringIO.StringIO(f.read(16384))
    
        header = _topsParseHeader(chunk)

        # remove the redundant top-level:
        header = header['WA Spectroscopy']
        # attach the header structure to our instance for later use 
        self._header = header
        
        ob.XRes = int(header['PointsX'])
        ob.YRes = int(header['PointsY'])
        ob.ImageType = {'Height':'Height',
                        'Current':'Current',
                        'DI/DX':'DI/DX'}[header['Image data']]
        ob.UBias = Decimal(header['Bias'].split(' ')[0])
        # As far as I can see, old and new software always write 0 nA here:
        ob.ISet = Decimal(header['Setpoint'].split(' ')[0])
        ob.Angle = Decimal(str(math.degrees(float(header['Rotate Ang.']))))
        
        # fill out the Z-sensitivity field, depending on type of data
        if ob.ImageType == 'Height':
            ob.ZScale = Decimal(header['Z sensitivity']) # nm/V
            ob.ZScale = ob.ZScale * Decimal('20.0') / Decimal('3276.8') # HV gain: 20
            ob.ZUnit = 'nm'
        if ob.ImageType == 'Current':
            ob.ZScale = Decimal('1000.0') / Decimal('3276.8')
            ob.ZUnit = 'nA'
        if ob.ImageType == 'DI/DX':
            ob.ZScale = Decimal('1.0') / Decimal('3276.8')
            ob.ZUnit = 'V'
        
        ob.XPos = Decimal(header['X offset'].split(' ')[0])
        ob.YPos = Decimal(header['Y offset'].split(' ')[0])
        ob.XSize = Decimal(header['Area'].split(' ')[0])
        ob.YSize = ob.XSize
        
        # these values are not always there:
        try:
            ob.LIMod = Decimal(header['Lockin modamp'])
            ob.LIOff = Decimal(header['Lockin offset'])
            ob.LIPhase = Decimal(header['Lockin phase'])
            ob.LISens = Decimal(header['Lockin sens'].split(' ')[0])
            ob.LITau = Decimal(header['Lockin tau'].split(' ')[0])
            ob.Temperature = Decimal(header['Temperature'])
        except KeyError:
            pass
        ob.Range = tuple(Decimal(part.strip().split(' ')[0]) for part in header['X range'].split('..'))
        f.close()

    def readData(self,ob):
        f = open(ob.filename,'rb')
        f.seek(int(self._header['Data offset']))
        points = int(self._header['SamplesT'])
        datalength = ob.XRes * ob.YRes * points * 2
        data = f.read(datalength)
        ob.d = scipy.fromstring(data,dtype=scipy.int16)
        ob.d.shape = ob.XRes, ob.YRes, points
        ob.d = scipy.flipud(ob.d)

def _topsParseHeader(file):
    """Read the text header of a TOPS format file.
    
    Returns a dictionary with a key for every section (lines with a * after the \)
    having another dictionary mapping names to values for every line in that section.
    
    So this::
    
        \*File list
        \Data length: 8192
        \Date: 11:24:41 AM Tue Jun 27 2006
        \Start context: 0L
    
    gives::
        header = {'File list':
                    {'Data length': 8192,
                     'Date': 11:24:41 AM Tue Jun 27 2006,
                     'Start context': '0L' } }
    """
    
    head = {}
    context = '.'
    for line in file:
        line = line.strip()
        if line[0] == '\\':
            if line[1] == '*':
                context = line[2:].strip()
                head[context] = {}
            else:
                key, value = [part.strip() for part in line[1:].split(':',1)]
                head[context][key] = value
    
    return head

