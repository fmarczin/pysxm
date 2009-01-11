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
import re
import scipy
import Data

def __parline(name,value):
	"""Format name and value as a parfile line

	Returns a string"""

	return name.ljust(32) + ': ' + value + '\n'

def write(filename,pages):
	"""Write the topography and current images in 'pages' to Omikron-style files"""

	root, ext = os.path.splitext(filename)
	path, base = os.path.split(root)
	print 'opening ' + root + '.par' + ' for writing'
	parfile = open(root + '.par','w')
	for firstimage in pages:
		if firstimage['type'] == 0:
			break
	parfile.write(';\n;               Omicron SPM Control.\n;           Parameter file for SPM data.\n;\n\n')
	parfile.write('Format                          : 1\n\n')
	parfile.write('Version                         : V2.2\n')
	parfile.write('System                          : SCALA\n\n')
	parfile.write('\n;\n; User Information.\n;\n\n')
	date = str.split(firstimage['strings']['date'],'/')
	parfile.write(__parline('Date',str.join('.',(date[1],date[0],date[2])) + ' ' + firstimage['strings']['time']))
	parfile.write(__parline('User','spm'))
	parfile.write(__parline('Comment',firstimage['strings']['user_text']))
	parfile.write('\n;\n; Scanner Description.\n;\n\n')
	parfile.write(__parline('Name','Converted from SM3-file'))
	parfile.write(__parline('VGAP Contact','SAMPLE'))
	parfile.write('\n;\n; Scanner Area Description.\n;\n\n')
	parfile.write(__parline('Field X Size in nm',str(firstimage['x_size']*firstimage['x_scale']*1000000000.0) + '     ;[nm]'))
	parfile.write(__parline('Field Y Size in nm',str(firstimage['y_size']*firstimage['y_scale']*1000000000.0) + '     ;[nm]'))
	parfile.write(__parline('Image Size in X',str(firstimage['x_size'])))
	parfile.write(__parline('Image Size in Y',str(firstimage['y_size'])))
	parfile.write(__parline('Increment X',str(firstimage['x_scale']*1000000000.0) + '     ;[nm]'))
	parfile.write(__parline('Increment Y',str(firstimage['y_scale']*1000000000.0) + '     ;[nm]'))
	parfile.write(__parline('Scan Angle',str(firstimage['angle']) + '     ;[Degree]'))
	parfile.write(__parline('X Offset',str(firstimage['x_offset']*1000000000.0) + '     ;[nm]'))
	parfile.write(__parline('Y Offset',str(firstimage['y_offset']*1000000000.0) + '     ;[nm]'))
	parfile.write('\n;\n; Topographic Channels.\n;\n\n')
	for page in pages:
		if page['type'] == 0:		# image
			if page['page_type'] == 1:	# topography
				displayname = 'Z'
				physunit = 'nm'
				extnum = '0'
			if page['page_type'] == 2:	# current
				displayname = 'Ext 1'
				physunit = 'V'
				extnum = '1'
			# RHK(right,down)  ->  Omikron(forward)
			if (page['scan'] == 0) or (page['scan'] == 2):
				direction = 'Forward'
				extletter = 'f'
				forwardpage = page
			else:
				direction = 'Backward'
				extletter = 'b'
				backwardpage = page
			pagebasename = base + '.t' + extletter + extnum
			page['basename'] = pagebasename
			print 'opening ' + os.path.join(path,pagebasename) + ' for writing'
			datafile = open(os.path.join(path,pagebasename),'wb')
			data = page['page_data'].astype(scipy.UInt16)
			data = data[::-1]
			data = data[:, ::-1]
#			data = transpose(data)
			data.byteswap()
			datafile.write(data.astype(scipy.UInt16))
			datafile.close()
			parfile.write('Topographic Channel'.ljust(32) + ': ' + displayname + '   ;Channel\n')
			parfile.write((' ' * 34) +  direction + '\n')
			parfile.write((' ' * 34) + '-32767   ;Minimum raw value\n')
			parfile.write((' ' * 34) + '32766   ;Maximum raw value\n')
			parfile.write((' ' * 34) + str(page['z_scale']*1000000000.0*(-32767.0)) + '   ;Minimum value in physical unit\n')
			parfile.write((' ' * 34) + str(page['z_scale']*1000000000.0*32766.0) + '   ;Maximum value in physical unit\n')
			parfile.write((' ' * 34) + str(page['z_scale']*1000000000.0) + '   ;Resolution\n')
			parfile.write((' ' * 34) + physunit + '   ;Physical unit\n')
			parfile.write((' ' * 34) + pagebasename + '   ;Filename\n')
			parfile.write((' ' * 34) + displayname.upper() + '   ;Display name\n')
			parfile.write('\n')
	parfile.write('\n;\n; Measurement parameters.\n;\n\n')
	parfile.write(__parline('SPM Method',': STM'))
	parfile.write(__parline('Dual mode','On'))
	parfile.write(__parline('Delay','30000     ;[us] (Forward)'))
	parfile.write((' ' * 34) +    '30000     ;[us] (Backward)\n')
	parfile.write(__parline('Gap Voltage', str(forwardpage['bias']) + '     ;[V] (Forward)'))
	parfile.write((' ' * 34) + str(backwardpage['bias']) + '     ;[V] (Forward)\n')
	parfile.write(__parline('Feedback Set', str(forwardpage['current']*1000000000.0) + '     ;[nA] (Forward)'))
	parfile.write((' ' * 34) + str(backwardpage['current']*1000000000.0) + '     ;[nA] (Backward)\n')
	parfile.write(__parline('Loog Gain','1.50000     ;[%] (Forward)'))
	parfile.write((' ' * 34) +        '1.50000     ;[%] (Backward)\n')
	parfile.write('X Resolution                    : 0     ;Currently not used.\n')
	parfile.write('Y Resolution                    : 0     ;Currently not used.\n')
	parfile.write(__parline('Scan Speed', str(forwardpage['x_scale']*1000000000.0/forwardpage['period']) + '     ;[nm/s]'))
	parfile.write('X Drift                         : 0.00000     ;[nm/s]\n')
	parfile.write('Y Drift                         : 0.00000     ;[nm/s]\n')
	parfile.write('Scan Mode                       : Frame\n')
	parfile.write('Topography Time per Point       : 0\n')
	parfile.write('Spectroscopy Grid Value in X    : 1\n')
	parfile.write('Spectroscopy Grid Value in Y    : 1\n')
	parfile.write('Spectroscopy Points in X        : 400\n')
	parfile.write('Spectroscopy Lines in Y         : 0\n')
	parfile.write('\n')
	parfile.write('\n;\n; Z Control Parameters.\n;\n\n')
	parfile.write('Z Speed                         : 1000.00     ;[nm/s]\n')
	parfile.write('Z Output Gain                   : 0.0100000\n')
	parfile.write('Automatic Z zero                : On')
	parfile.write('Z Input Gain                    : 1.0000\n')
	parfile.close()

def readparfile(fname):
    parfile = open(fname,'r')
    common = {}
    channels = []
    re_emptyline = re.compile(r'^\s*$')
    re_channelstart = re.compile(r'^Topographic Channel')
    re_comment = re.compile(r'^Comment')

    lineno = 0
    line = parfile.readline()
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
    return (common,channels)

def pickValueForMode(com, chan, field):
    if com['Dual mode'] == 'On':
        if chan['direction'] == 'Forward':
            return com[field][0]
        else:
            return com[field][1]
    else:
        return com[field]


def readdatafile(fname):
    root, ext = os.path.splitext(fname)
    path, base = os.path.split(root)
    datafilename = base + ext
    parfile = root + '.par'
    
    (common, channels) = readparfile(parfile)

    channelindex = [n for n,d in enumerate(channels) if d['file'] == datafilename][0]
    thechannel = channels[channelindex]
    
    i = Data.Image()
    i.Name = datafilename
    i.ImageType = 'Topo'
    i.XPos = float(common['X Offset'])
    i.YPos = float(common['Y Offset'])
    i.XSize = float(common['Field X Size in nm'])
    i.YSize = float(common['Field Y Size in nm'])
    i.XRes = int(common['Image Size in X'])
    i.YRes = int(common['Image Size in Y'])
    i.ZScale = (float(thechannel['maxphys']) - float(thechannel['minphys'])) / \
        (float(thechannel['maxraw']) - float(thechannel['minraw']))
    i.UBias = float(pickValueForMode(common,thechannel,'Gap Voltage'))
    i.ISet = float(pickValueForMode(common,thechannel,'Feedback Set'))
    i.ScanSpeed = float(common['Scan Speed'])
    i.d = scipy.fromfile(file=fname,dtype=scipy.int16)
    i.d = i.d.byteswap()
    i.d.shape = i.XRes, i.YRes
    i.updateDataRange()
    return i
    
