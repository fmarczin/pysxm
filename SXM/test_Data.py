# Copyright 2008,2009 Felix Marczinowski <fmarczin@physnet.uni-hamburg.de>
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
""""Test module for SXM.Data"""

from SXM.Data import DataField
import scipy

def setup_module(m):
    m.TestData.df = DataField([-3, 1, 3, -1])

class TestData:

    def test_inithasdatafield(self):
        assert hasattr(self.df,'d')
        
    def test_initdisndarray(self):
        n = scipy.array([])
        assert (type(self.df.d) == type(n))

    def test_range(self):
        self.df.updateDataRange()
        assert  ([-3, 3] == [self.df.dataMin, self.df.dataMax])
