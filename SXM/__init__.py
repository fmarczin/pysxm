"""Package of SXM-related code.

G{packagetree}
"""

import FileIO
from FileIO import loadFile
FileIO.init()

import Data

def open(fname):
    """Open S(X)M data from fname.
    """
    return FileIO.fromFile(fname).load()


__all__ = ['Data','FileIO']
