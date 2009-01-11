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
"""Module for reading .sm3 files"""
import os
import sys
import struct
import scipy
import math
import Data

# Types:
(TImage,TLineSpect,TReserved,TAnnotatedLineSpect) = range(4)
# PageTypes:
(PTUndef,PTTopography,PTCurrent,PTAux,PTForce,PTSignal,PTImageFFT,
	PTNoisePowerSpectrum,PTLineTest,PTOscilloscope,PTIVSpectra,PTImageIV4x4,
	PTImageIV8x8,PTImageIV16x16,PTImageIV32x32,PTImageIVCenter,
	PTImageInteractiveSpectra,PTAutocorrelationPage,PTIZSpectra,
	PT4GainTopography,PT8GainTopography,PT4GainCurrent,PT8GainCurrent,
	PTImageIV64x64,PTAutocorrelationSpectrum,PTCounterData,
	PTMultichannelData,PTAFM100,PTCITS,PTGPIB,PTVideo,PTIout,PTIdatalog,
    PTIEcset,PTIEcdata,PTIDSPAD,PTDiscSpecPres,PTImDiscSpec,PTRampSpecRel,
    PTDiscSpecRel) = range(40)
# LineTypes:
(LTNotALine,LTHistogram,LTCrossSection,LTLineTest,LTOscilloscope,LTReserved,
	LTNoisePowerSpec,LTIVSpectrum,LTIZSpectrum,LTImageXAverage,
	LTImageYAverage,LTNoiseAutocorrelation,LTMultichannelData,LTVarGapIV,
	LTImageHistogramSpectra,LTImageCrossSection,LTImageAverage,LTCrossSec,
    LTGoutspec,LTGdatalog,LTGxy,LTGechem,LTGDiscspec_data) = range(23)
# SourceTyes:
(SRaw,SProcessed,SCalculated,SImported) = range(4)
# ImageTypes:
(ITNormalImage,ITAutocorrelationImage) = range(2)
# Scan directions:
(ScanRight,ScanLeft,ScanUp,ScanDown) = range(4)

def __read_pageheader(fh):
	"""Read a SM3 PAGE HEADER structure from filehandle fh

	Returns the unpacked header as a dictionary, or None if there was no
	valid header"""

	size = struct.unpack('<h36s',fh.read(38))[0]
	phbin = fh.read(size-36)
	if size >= 160:
		hd = struct.unpack('<h12iLllfffffffffff4L',phbin[:158])
		header_keys = ('version', 'string_count', 'type',
			'page_type', 'data_sub_source', 'line_type', 'x_coordinate',
			'y_coordinate', 'x_size', 'y_size', 'source_type', 'image_type',
			'scan', 'group_id', 'page_data_size', 'z_minimum_value',
			'z_maximum_value', 'x_scale', 'y_scale', 'z_scale', 'xy_scale',
			'x_offset', 'y_offset', 'z_offset', 'period', 'bias', 'current',
			'angle', 'guid1', 'guid2', 'guid3', 'guid4')
		ph = dict(zip(header_keys, hd))
		ph['x_scale'] = math.fabs(ph['x_scale'])
		ph['y_scale'] = math.fabs(ph['y_scale'])
		ph['z_scale'] = math.fabs(ph['z_scale'])
		ph['version'] = unicode(ph['version'],'utf-16').encode('ascii')
		return ph
	return None

def __read_strings(fh):
	"""Read a SM3 STRINGS structure from filehandle fh

	Reads the 12 standard strings
	Returns the found strings in a dictionary with the usual sm3 string names"""

	strings = {}
	for stringname in ('label', 'system_text', 'session_text', 'user_text',
		'path', 'date', 'time', 'x_units', 'y_units', 'z_units',
		'x_label', 'y_label'):
		len = 2 * (struct.unpack('h',fh.read(2)))[0]
		strings[stringname] = unicode(fh.read(len),'utf-16').encode('ascii')
	return strings

def __read_colorinfo(fh):
	"""Read a SM3 COLOR INFO structure from filehandle fh

	Returns the raw data or None if param_size was 0"""

	size = struct.unpack('<h',fh.read(2))[0]
	if size > 0:
		return fh.read(size)
	else:
		return None

def __read_pagedata(fh,page):
	"""Read a SM3 PAGE DATA block from filehandle fh

	Returns the data interpreted as Int32 (32 bit signed, little-endian)
	and shaped into an array according to x_size and y_size given in page"""

	data = fh.read(page['page_data_size'])
	data = scipy.fromstring(data,scipy.int32)
#	data -= data.min()
	data.shape = page['x_size'], page['y_size']
	return data

def __read_spectraldata(fh,y_size):
	"""Read a SM3 SPECTRAL DATA structure from filehandle fh

	Returns the raw data"""

	return fh.read(y_size*4)

def read_page(fh):
	"""Read a SM3 PAGE from filehandle fh
	
	This function accepts an open file, from which it reads a page header and, 
	using the information found there, read the according subsequent data blocks
	Returns the page as a dictionary"""

	page = {}
	page = __read_pageheader(fh)
	page['strings'] = __read_strings(fh)
	page['page_data'] = __read_pagedata(fh,page)
	if page['type'] == TImage:
		# page contains an image
		page['color_info'] = __read_colorinfo(fh)
# 		figure(num=1,figsize=(5,5))
# 		axes([0.1,0.1,0.8,0.8])
# 		im = imshow(page['page_data'], cmap=cm.jet, origin='lower', extent=(0,page['x_size'],0,page['y_size']))
# 		levels, colls = contour(range(page['x_size']), range(page['y_size']), page['page_data'], 10, colors=('k',))
#		clabel(colls, levels, fontsize=9, inline=1)
# 		show()
	if page['type'] in (TLineSpect,TAnnotatedLineSpect):
		# page contains a spectrum
		page['spectral_data'] = __read_spectraldata(fh,page['y_size'])
	return page

def read_pagen(filename,index=1):
    """Read the index'th SM3 PAGE from file filename.
    
    index starts from 0
    """
    # TODO: only read req'ed page, right now it reads and parses every page up to "index"
    f = open(filename,'rb')
    for i in range(index+1):
        p = read_page(f)
    
    im = Data.Image()
    (im.Name,dummy) = os.path.splitext(os.path.basename(filename))
    im.ImageType = "Topo"
    im.d = p['page_data']
    im.XPos = p['x_coordinate']
    im.YPos = p['y_coordinate']
    im.XRes = p['x_size']
    im.YRes = p['y_size']
    im.XScale = p['x_scale']
    im.YScale = p['y_scale']
    im.ZScale = p['z_scale']
    im.UBias = p['bias']
    im.ISet = p['current']
    return im
