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
