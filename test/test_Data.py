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
import unittest
import Data

class DataFieldTest(unittest.TestCase):
   def setUp(self):
      self.df = Data.DataField([-3, 1, 3, -1])
      self.assertNotEqual(self.df, None)

   def testRange(self):
      self.df.updateDataRange()
      self.assertEqual([-3, 3], [self.df.dataMin, self.df.dataMax])

if __name__ == "__main__":
   unittest.main()
