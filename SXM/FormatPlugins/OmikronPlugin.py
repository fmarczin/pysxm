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
from SXM import Data,FileIO
import scipy
import os
import re

class OmikronTopoReader(FileIO.FormatReader):
    """Reader for Omikron 2D images.
    
    """
    description = 'Omikron Image'
    format = 'SCALA'
    patterns = ('*.tf?','*.tb?')
    datatype = Data.Image
    
    def __init__(self):
        FileIO.FormatReader.__init__(self)
        self._header = []

    def readHeader(self,ob):
        root, ext = os.path.splitext(ob.filename)
        path, base = os.path.split(root)
        
        ob.Name = base + ext
        ob.Method = 'STM'

        datafilename = base + ext
        parfile = root + '.par'
        
        (common, channels) = _readparfile(parfile)
    
        channelindex = [n for n,d in enumerate(channels) if d['file'] == datafilename][0]
        thechannel = channels[channelindex]
        
        ob.Name = datafilename
        ob.ImageType = 'Height'
        ob.XPos = float(common['X Offset'])
        ob.YPos = float(common['Y Offset'])
        ob.XSize = float(common['Field X Size in nm'])
        ob.YSize = float(common['Field Y Size in nm'])
        ob.XRes = int(common['Image Size in X'])
        ob.YRes = int(common['Image Size in Y'])
        ob.ZScale = (float(thechannel['maxphys']) - float(thechannel['minphys'])) / \
            (float(thechannel['maxraw']) - float(thechannel['minraw']))
        ob.UBias = float(_pickValueForMode(common,thechannel,'Gap Voltage'))
        ob.ISet = float(_pickValueForMode(common,thechannel,'Feedback Set'))
        ob.ScanSpeed = float(common['Scan Speed'])

    def readData(self,ob):
        ob.d = scipy.fromfile(file=ob.filename,dtype=scipy.int16)
        ob.d = ob.d.byteswap()
        ob.d.shape = ob.XRes, ob.YRes
        ob.updateDataRange()

def _readparfile(fname):
    parfile = open(fname,'r')
    common = {}
    channels = []
    re_emptyline = re.compile(r'^\s*$')
    re_channelstart = re.compile(r'^Topographic Channel')
    re_comment = re.compile(r'^Comment')

    lineno = 0
    line = parfile.readline()
    try:
        while len(line) > 0:
            line = line.split(';')[0]   # use only the part before the first ';'
            if not (re_emptyline.match(line)):
                if re_channelstart.match(line):
                    channel = {}
                    channel['channel'] = line.split(':')[1].strip()
                    channel['direction'] = parfile.readline().split(';')[0].strip()
                    channel['minraw'] = parfile.readline().split(';')[0].strip()
                    channel['maxraw'] = parfile.readline().split(';')[0].strip()
                    channel['minphys'] = parfile.readline().split(';')[0].strip()
                    channel['maxphys'] = parfile.readline().split(';')[0].strip()
                    channel['res'] = parfile.readline().split(';')[0].strip()
                    channel['unit'] = parfile.readline().split(';')[0].strip()
                    channel['file'] = parfile.readline().split(';')[0].strip()
                    channel['name'] = parfile.readline().split(';')[0].strip()
                    channels.append(channel)
                else:
                    if re_comment.match(line):
                        comment = line.split(':')[1].strip() + '\n'
                        line = parfile.readline().split(';')[0]
                        while len(line) > 0:
                            comment += line + '\n'
                            line = parfile.readline().split(';')[0].strip()
                    else:
                        (name, value) = line.split(':',1)
                        name = name.strip()
                        value = value.strip()
                        common[name] = value
                        if name in ('Delay','Gap Voltage','Feedback Set','Loop Gain'):
                            if common.has_key('Dual mode') and (common['Dual mode'] == 'On'):
                                line = parfile.readline().split(';')[0].strip()
                                common[name] = (common[name], line)
            line = parfile.readline()
    except ValueError:
        print(line)
        raise
    return (common,channels)

def _pickValueForMode(com, chan, field):
    if com['Dual mode'] == 'On':
        if chan['direction'] == 'Forward':
            return com[field][0]
        else:
            return com[field][1]
    else:
        return com[field]

