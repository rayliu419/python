# guide how to use lib in app directory.

import sys
sys.path.append(r"../lib")

from date import *

print(getYesterday())